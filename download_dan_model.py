from __future__ import annotations

import argparse
import html
import re
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Optional


FILE_ID = "1uHNADViICyJEjJljv747nfvrGu12kjtu"
FILE_NAME = "affecnet8_epoch5_acc0.6209.pth"
MIN_EXPECTED_BYTES = 10 * 1024 * 1024


class DriveDownloadFormParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.form_action: Optional[str] = None
        self.form_method: str = "get"
        self.hidden_inputs: dict[str, str] = {}
        self._in_target_form = False

    def handle_starttag(self, tag: str, attrs) -> None:
        attributes = {key: value for key, value in attrs}
        if tag.lower() == "form":
            form_id = (attributes.get("id") or "").strip().lower()
            if form_id == "download-form":
                self._in_target_form = True
                self.form_action = attributes.get("action")
                self.form_method = (attributes.get("method") or "get").lower()
            return

        if not self._in_target_form or tag.lower() != "input":
            return

        input_type = (attributes.get("type") or "").strip().lower()
        name = attributes.get("name")
        value = attributes.get("value") or ""
        if input_type == "hidden" and name:
            self.hidden_inputs[name] = value

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "form" and self._in_target_form:
            self._in_target_form = False


def _build_opener(use_system_proxy: bool) -> urllib.request.OpenerDirector:
    cookie_jar = CookieJar()
    handlers = [
        urllib.request.HTTPCookieProcessor(cookie_jar),
    ]
    if use_system_proxy:
        handlers.append(urllib.request.ProxyHandler())
    else:
        handlers.append(urllib.request.ProxyHandler({}))
    return urllib.request.build_opener(*handlers)


def _headers() -> dict[str, str]:
    return {
        "User-Agent": "Mozilla/5.0",
    }


def _looks_like_html_bytes(content: bytes) -> bool:
    prefix = content[:512].lstrip().lower()
    return (
        prefix.startswith(b"<!doctype html")
        or prefix.startswith(b"<html")
        or b"<html" in prefix
    )


def _read_prefix(path: Path, size: int = 1024) -> bytes:
    with path.open("rb") as handle:
        return handle.read(size)


def _is_valid_checkpoint(path: Path) -> bool:
    if not path.exists() or not path.is_file():
        return False
    if path.stat().st_size < MIN_EXPECTED_BYTES:
        try:
            if _looks_like_html_bytes(_read_prefix(path)):
                return False
        except Exception:
            return False
        return False
    try:
        return not _looks_like_html_bytes(_read_prefix(path))
    except Exception:
        return False


def _stream_download(response, output_path: Path) -> None:
    total = response.headers.get("Content-Length")
    total_bytes = int(total) if total and total.isdigit() else None
    downloaded = 0
    chunk_size = 1024 * 1024

    with output_path.open("wb") as handle:
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            handle.write(chunk)
            downloaded += len(chunk)
            if total_bytes:
                percent = downloaded / total_bytes * 100
                print(f"\rDownloading {FILE_NAME}: {percent:6.2f}%", end="", flush=True)
            else:
                mb = downloaded / (1024 * 1024)
                print(f"\rDownloading {FILE_NAME}: {mb:.2f} MB", end="", flush=True)
    print()


def _response_is_attachment(response) -> bool:
    content_disposition = response.headers.get("Content-Disposition", "")
    if "attachment" in content_disposition.lower():
        return True
    content_type = (response.headers.get("Content-Type") or "").lower()
    return "application/octet-stream" in content_type


def _read_html(response) -> str:
    return response.read().decode("utf-8", errors="ignore")


def _extract_confirm_token(html_text: str) -> str | None:
    patterns = [
        r'name="confirm"\s+value="([^"]+)"',
        r"confirm=([0-9A-Za-z_]+)&amp;id=",
        r"confirm=([0-9A-Za-z_]+)&id=",
    ]
    for pattern in patterns:
        match = re.search(pattern, html_text)
        if match:
            return html.unescape(match.group(1))
    return None


def _parse_download_form(html_text: str, fallback_url: str) -> tuple[str, dict[str, str]] | None:
    parser = DriveDownloadFormParser()
    parser.feed(html_text)
    if parser.form_action and parser.hidden_inputs:
        action_url = urllib.parse.urljoin(fallback_url, parser.form_action)
        return action_url, dict(parser.hidden_inputs)
    return None


def _build_confirm_request(first_html: str, base_url: str) -> tuple[str, dict[str, str]]:
    parsed_form = _parse_download_form(first_html, base_url)
    if parsed_form is not None:
        return parsed_form

    confirm_token = _extract_confirm_token(first_html)
    if confirm_token:
        return (
            "https://drive.google.com/uc",
            {
                "export": "download",
                "confirm": confirm_token,
                "id": FILE_ID,
            },
        )

    raise RuntimeError(
        "Failed to parse Google Drive confirmation page. "
        "Open the file page manually if needed: "
        f"https://drive.google.com/file/d/{FILE_ID}/view?usp=sharing"
    )


def _request_download(opener: urllib.request.OpenerDirector, use_system_proxy: bool) -> object:
    base_url = "https://drive.google.com/uc?export=download&id=" + FILE_ID
    print(
        "Using system proxy:" if use_system_proxy else "Using direct connection (proxy disabled):",
        use_system_proxy,
    )
    first_request = urllib.request.Request(base_url, headers=_headers())
    first_response = opener.open(first_request)
    if _response_is_attachment(first_response):
        return first_response

    first_html = _read_html(first_response)
    confirm_url, form_fields = _build_confirm_request(first_html, base_url)
    query = urllib.parse.urlencode(form_fields)
    separator = "&" if "?" in confirm_url else "?"
    download_url = confirm_url + separator + query
    confirm_request = urllib.request.Request(download_url, headers=_headers())
    return opener.open(confirm_request)


def download_dan_checkpoint(output_dir: Path, *, use_system_proxy: bool) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / FILE_NAME

    if _is_valid_checkpoint(output_path):
        print(f"Checkpoint already exists: {output_path}")
        return output_path

    if output_path.exists():
        print(f"Removing invalid existing file: {output_path}")
        output_path.unlink()

    opener = _build_opener(use_system_proxy=use_system_proxy)
    response = _request_download(opener, use_system_proxy=use_system_proxy)
    if not _response_is_attachment(response):
        body = response.read()
        if _looks_like_html_bytes(body):
            snippet = body[:500].decode("utf-8", errors="ignore")
            raise RuntimeError(
                "Google Drive returned HTML instead of the DAN checkpoint. "
                "This usually means the confirmation flow changed again or the network/proxy intercepted the request. "
                f"HTML preview: {snippet}"
            )
        raise RuntimeError("Download response is not a file attachment.")

    _stream_download(response, output_path)
    if not _is_valid_checkpoint(output_path):
        size = output_path.stat().st_size if output_path.exists() else 0
        raise RuntimeError(
            f"Downloaded file is invalid or incomplete: {output_path} (size={size} bytes)"
        )
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Download DAN AffectNet-8 checkpoint")
    default_output = Path(__file__).resolve().parent / "backend" / "models" / "emotion"
    parser.add_argument(
        "--output-dir",
        default=str(default_output),
        help="Directory to store the DAN checkpoint",
    )
    parser.add_argument(
        "--use-system-proxy",
        action="store_true",
        help="Use HTTP_PROXY / HTTPS_PROXY and system proxy settings instead of forcing direct connection",
    )
    args = parser.parse_args()

    output_path = download_dan_checkpoint(
        Path(args.output_dir),
        use_system_proxy=args.use_system_proxy,
    )
    print(f"DAN checkpoint saved to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
