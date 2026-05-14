<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import {
  checkinAttendance,
  exportAttendanceRecords,
  fetchAttendanceRecords,
} from "../api/attendance";
<<<<<<< HEAD
import TeacherHeader from "../components/TeacherHeader.vue";
=======
import { createLivenessChallenge } from "../api/liveness";
import TeacherHeader from "../components/TeacherHeader.vue";
import { formatEmotion as formatEmotionLabel } from "../constants/emotions";
>>>>>>> 98bf8e49 (update)
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();
const videoRef = ref(null);
const canvasRef = ref(null);
const streamRef = ref(null);
const autoTimerRef = ref(null);

const user = ref(null);
const loadingRecords = ref(false);
const processing = ref(false);
const cameraReady = ref(false);
const autoMode = ref(false);
const activeTab = ref("capture");
<<<<<<< HEAD
const statusText = ref("等待开启摄像头");
const lastSnapshot = ref("");

const BURST_FRAME_COUNT = 5;
const BURST_INTERVAL_MS = 220;

const result = ref(null);
const records = ref([]);
=======
const challengeModeEnabled = ref(false);
const statusText = ref("等待开启摄像头");
const lastSnapshot = ref("");
const result = ref(null);
const records = ref([]);
const currentChallenge = ref(null);

const FRAME_INTERVAL_MS = 220;
const ACTION_READY_DELAY_MS = 900;
const AUTO_INTERVAL_MS = 10000;
const PASSIVE_FRAME_COUNT = 5;
>>>>>>> 98bf8e49 (update)

const filters = reactive({
  keyword: "",
  class_name: "",
  status: "",
  capture_mode: "",
  liveness_result: "",
  start_date: "",
  end_date: "",
});

const statistics = computed(() => {
  const base = {
    total: records.value.length,
    present: 0,
    unknown: 0,
    rejected: 0,
  };
  for (const item of records.value) {
    if (item.status === "present") base.present += 1;
    if (item.status === "unknown") base.unknown += 1;
    if (item.status === "rejected") base.rejected += 1;
  }
  return base;
});

<<<<<<< HEAD
=======
const challengeModeLabel = computed(() =>
  challengeModeEnabled.value ? "随机动作增强：已开启" : "随机动作增强：已关闭",
);

const challengeModeType = computed(() =>
  challengeModeEnabled.value ? "warning" : "info",
);

>>>>>>> 98bf8e49 (update)
function setStatus(text) {
  statusText.value = text;
}

function sleep(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function resetAutoCapture() {
  if (autoTimerRef.value) {
    window.clearInterval(autoTimerRef.value);
    autoTimerRef.value = null;
  }
}

<<<<<<< HEAD
=======
function formatStatus(status) {
  const labelMap = {
    present: "成功",
    unknown: "未匹配",
    rejected: "拒绝",
    retry: "重试",
  };
  return labelMap[status] || status || "-";
}

function formatCaptureMode(mode) {
  return mode === "auto" ? "自动" : "手动";
}

function formatLivenessResult(value) {
  const labelMap = {
    real: "真人",
    fake: "未通过",
    uncertain: "待重试",
  };
  return labelMap[value] || value || "-";
}

function formatChallengeResult(value) {
  const labelMap = {
    passed: "通过",
    failed: "未通过",
    uncertain: "待重试",
    skipped: "未启用",
  };
  return labelMap[value] || value || "-";
}

function formatVerificationMode(mode) {
  const labelMap = {
    passive_anti_spoof: "被动活体",
    passive_anti_spoof_fused: "被动活体融合",
    passive_plus_challenge: "被动活体 + 随机动作",
    random_action_challenge: "随机动作",
  };
  return labelMap[mode] || mode || "-";
}

function formatEmotion(value) {
  return formatEmotionLabel(value);
}

function statusTagType(status) {
  if (status === "present") return "success";
  if (status === "rejected") return "danger";
  if (status === "retry") return "warning";
  return "info";
}

function livenessTagType(value) {
  if (value === "real") return "success";
  if (value === "fake") return "danger";
  return "warning";
}

function challengeTagType(value) {
  if (value === "passed") return "success";
  if (value === "failed") return "danger";
  if (value === "uncertain") return "warning";
  return "info";
}

>>>>>>> 98bf8e49 (update)
function stopCamera() {
  resetAutoCapture();
  const stream = streamRef.value;
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
  }
  streamRef.value = null;
  cameraReady.value = false;
  autoMode.value = false;
<<<<<<< HEAD
=======
  currentChallenge.value = null;
>>>>>>> 98bf8e49 (update)
  setStatus("摄像头已关闭");
}

async function startCamera() {
  try {
    stopCamera();
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        facingMode: "user",
      },
      audio: false,
    });
    streamRef.value = stream;
    videoRef.value.srcObject = stream;
    cameraReady.value = true;
<<<<<<< HEAD
    setStatus("摄像头已开启，请保持正视镜头并轻微眨眼或转头");
=======
    setStatus(
      challengeModeEnabled.value
        ? "摄像头已开启，可开始考勤。当前为被动活体 + 随机动作增强模式"
        : "摄像头已开启，可开始考勤。当前为默认被动活体模式",
    );
>>>>>>> 98bf8e49 (update)
  } catch (error) {
    cameraReady.value = false;
    setStatus("摄像头调用失败，请检查浏览器权限");
    ElMessage.error(error.message || "摄像头调用失败");
  }
}

<<<<<<< HEAD
async function captureBurstBlobs() {
  const video = videoRef.value;
  const canvas = canvasRef.value;
  if (!video || !canvas) {
    throw new Error("视频组件未准备完成");
=======
async function captureFrames(count, saveLastSnapshot = false) {
  const video = videoRef.value;
  const canvas = canvasRef.value;
  if (!video || !canvas) {
    throw new Error("视频组件尚未准备完成");
>>>>>>> 98bf8e49 (update)
  }
  if (!video.videoWidth || !video.videoHeight) {
    throw new Error("摄像头画面尚未就绪");
  }

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const context = canvas.getContext("2d");
  const blobs = [];

<<<<<<< HEAD
  for (let index = 0; index < BURST_FRAME_COUNT; index += 1) {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    if (index === BURST_FRAME_COUNT - 1) {
      lastSnapshot.value = canvas.toDataURL("image/png");
    }
    const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
    blobs.push(blob);
    if (index < BURST_FRAME_COUNT - 1) {
      await sleep(BURST_INTERVAL_MS);
    }
  }
  return blobs;
}

async function captureFrame(captureMode = "manual") {
  if (!cameraReady.value || processing.value) {
    return;
  }

  processing.value = true;
  setStatus(
    captureMode === "auto"
      ? `自动抓拍中，正在采集 ${BURST_FRAME_COUNT} 帧`
      : `手动抓拍中，正在采集 ${BURST_FRAME_COUNT} 帧`
  );

  try {
    const blobs = await captureBurstBlobs();
    setStatus("连续帧已采集，正在做时序活体检测与识别");
    const response = await checkinAttendance({ blobs, captureMode });
    result.value = response.data;

    if (response.data.status === "present") {
      setStatus(`考勤成功：${response.data.student_name}`);
      ElMessage.success(`考勤成功：${response.data.student_name}`);
    } else if (response.data.status === "rejected") {
      setStatus("活体检测未通过，已拒绝考勤");
      ElMessage.warning("活体检测未通过，已拒绝考勤");
    } else {
      setStatus("未匹配到已知学生");
      ElMessage.warning("未匹配到已知学生");
    }

    await loadRecords();
  } catch (error) {
    const message =
      error.response?.data?.message || error.message || "连续抓拍识别失败";
    setStatus(message);
    ElMessage.error(message);
  } finally {
    processing.value = false;
  }
}

function toggleAutoCapture() {
  if (!cameraReady.value) {
    ElMessage.warning("请先开启摄像头");
    autoMode.value = false;
    return;
  }

  if (autoMode.value) {
    resetAutoCapture();
    autoTimerRef.value = window.setInterval(() => {
      if (!processing.value) {
        captureFrame("auto");
      }
    }, 6000);
    setStatus("自动抓拍已开启，每 6 秒进行一次 5 帧活体检测");
  } else {
    resetAutoCapture();
    setStatus("自动抓拍已关闭");
  }
}

=======
  for (let index = 0; index < count; index += 1) {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    if (saveLastSnapshot && index === count - 1) {
      lastSnapshot.value = canvas.toDataURL("image/png");
    }
    const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
    if (!blob) {
      throw new Error("截图失败，请重试");
    }
    blobs.push(blob);
    if (index < count - 1) {
      await sleep(FRAME_INTERVAL_MS);
    }
  }

  return blobs;
}

>>>>>>> 98bf8e49 (update)
function buildQuery() {
  return {
    keyword: filters.keyword || undefined,
    class_name: filters.class_name || undefined,
    status: filters.status || undefined,
    capture_mode: filters.capture_mode || undefined,
    liveness_result: filters.liveness_result || undefined,
    start_date: filters.start_date || undefined,
    end_date: filters.end_date || undefined,
  };
}

async function loadRecords() {
  loadingRecords.value = true;
  try {
    const response = await fetchAttendanceRecords(buildQuery());
    records.value = response.data;
  } catch (error) {
<<<<<<< HEAD
    const message = error.response?.data?.message || "考勤记录加载失败";
    ElMessage.error(message);
=======
    ElMessage.error(error.response?.data?.message || "考勤记录加载失败");
>>>>>>> 98bf8e49 (update)
  } finally {
    loadingRecords.value = false;
  }
}

function resetFilters() {
  filters.keyword = "";
  filters.class_name = "";
  filters.status = "";
  filters.capture_mode = "";
  filters.liveness_result = "";
  filters.start_date = "";
  filters.end_date = "";
  loadRecords();
}

async function downloadRecords() {
  try {
    const response = await exportAttendanceRecords(buildQuery());
    const blob = new Blob([response.data], {
      type: response.headers["content-type"],
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    const disposition = response.headers["content-disposition"] || "";
    const match = disposition.match(/filename="?([^"]+)"?/);
    link.href = url;
    link.download = match?.[1] || "attendance_export.xlsx";
    link.click();
    window.URL.revokeObjectURL(url);
    ElMessage.success("导出成功");
  } catch (error) {
<<<<<<< HEAD
    const message = error.response?.data?.message || "导出失败";
    ElMessage.error(message);
=======
    ElMessage.error(error.response?.data?.message || "导出失败");
  }
}

async function requestChallenge() {
  const response = await createLivenessChallenge({ purpose: "attendance" });
  currentChallenge.value = response.data;
  return response.data;
}

function toggleChallengeMode() {
  challengeModeEnabled.value = !challengeModeEnabled.value;
  currentChallenge.value = null;
  setStatus(
    challengeModeEnabled.value
      ? "已开启随机动作增强。开始考勤后会先做被动活体，再叠加随机动作校验"
      : "已关闭随机动作增强。开始考勤后将直接做默认被动活体检测",
  );
}

function buildAttendanceMessage(payload) {
  if (payload.status === "present") {
    return payload.reason || `考勤成功：${payload.student_name || "已识别"}`;
  }
  if (payload.status === "retry") {
    return payload.challenge_reason || payload.reason || "当前样本需要重试";
  }
  if (payload.status === "rejected") {
    return payload.challenge_reason || payload.reason || "活体验证未通过";
  }
  return payload.reason || "活体验证通过，但未匹配到已知学生";
}

async function runAttendance(captureMode = "manual") {
  if (!cameraReady.value || processing.value) {
    return;
  }

  processing.value = true;
  result.value = null;
  try {
    let blobs = [];
    let challengeId;

    if (challengeModeEnabled.value) {
      const challenge = await requestChallenge();
      const baselineCount = challenge.baseline_frame_count || 3;
      const actionCount = challenge.action_frame_count || 6;

      setStatus("已生成随机动作，请先正视摄像头");
      const baselineBlobs = await captureFrames(baselineCount);

      setStatus(`请执行动作：${challenge.challenge_action_label}`);
      await sleep(ACTION_READY_DELAY_MS);
      const actionBlobs = await captureFrames(actionCount, true);

      blobs = [...baselineBlobs, ...actionBlobs];
      challengeId = challenge.challenge_id;
    } else {
      currentChallenge.value = null;
      setStatus("正在采集 5 帧图像并执行多帧被动活体检测");
      blobs = await captureFrames(PASSIVE_FRAME_COUNT, true);
    }

    const response = await checkinAttendance({
      blobs,
      captureMode,
      challengeId,
    });
    result.value = response.data;

    const message = buildAttendanceMessage(response.data);
    setStatus(message);
    if (response.data.status === "present") {
      ElMessage.success(message);
    } else if (response.data.status === "rejected") {
      ElMessage.warning(message);
    } else {
      ElMessage.info(message);
    }

    await loadRecords();
  } catch (error) {
    const message = error.response?.data?.message || error.message || "考勤失败";
    setStatus(message);
    ElMessage.error(message);
  } finally {
    processing.value = false;
  }
}

function toggleAutoCapture() {
  if (!cameraReady.value) {
    ElMessage.warning("请先开启摄像头");
    autoMode.value = false;
    return;
  }

  if (autoMode.value) {
    resetAutoCapture();
    autoTimerRef.value = window.setInterval(() => {
      if (!processing.value) {
        runAttendance("auto");
      }
    }, AUTO_INTERVAL_MS);
    setStatus(
      challengeModeEnabled.value
        ? "自动考勤已开启，系统会周期性执行被动活体 + 随机动作考勤"
        : "自动考勤已开启，系统会周期性执行被动活体考勤",
    );
  } else {
    resetAutoCapture();
    setStatus("自动考勤已关闭");
>>>>>>> 98bf8e49 (update)
  }
}

async function logout() {
  stopCamera();
  await performLogout(router);
}

<<<<<<< HEAD
function statusTagType(status) {
  if (status === "present") return "success";
  if (status === "rejected") return "danger";
  return "warning";
}

function livenessTagType(value) {
  if (value === "real") return "success";
  if (value === "fake") return "danger";
  return "info";
}

function openSecurityPage() {
  router.push({ name: "security-tests" });
}

function openStudentsPage() {
  router.push({ name: "students" });
}

function openGroupPhotosPage() {
  router.push({ name: "group-photos" });
}

function openEmotionPage() {
  router.push({ name: "emotions" });
}

function openReportPage() {
  router.push({ name: "report" });
}

function openUsersPage() {
  router.push({ name: "users" });
}

function openAuditLogsPage() {
  router.push({ name: "audit-logs" });
}

function openTeacherProfilePage() {
  router.push({ name: "teacher-profile" });
}

function openSystemStatusPage() {
  router.push({ name: "system-status" });
}

=======
>>>>>>> 98bf8e49 (update)
onMounted(async () => {
  user.value = parseSavedUser();
  await loadRecords();
});

onBeforeUnmount(() => {
  stopCamera();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="考勤" current="attendance" :user="user" @logout="logout" />

    <section class="stats-grid">
      <article class="stat-card">
        <span>总记录</span>
        <strong>{{ statistics.total }}</strong>
      </article>
      <article class="stat-card success">
        <span>考勤成功</span>
        <strong>{{ statistics.present }}</strong>
      </article>
      <article class="stat-card warning">
        <span>未匹配</span>
        <strong>{{ statistics.unknown }}</strong>
      </article>
      <article class="stat-card danger">
<<<<<<< HEAD
        <span>活体拒绝</span>
=======
        <span>拦截记录</span>
>>>>>>> 98bf8e49 (update)
        <strong>{{ statistics.rejected }}</strong>
      </article>
    </section>

    <el-tabs v-model="activeTab" class="main-tabs">
<<<<<<< HEAD
      <el-tab-pane label="实时考勤" name="capture">
        <div class="capture-grid">
          <section class="panel">
            <div class="panel-head">
              <h2>摄像头采集区</h2>
              <span class="status-badge">{{ statusText }}</span>
            </div>
=======
      <el-tab-pane label="考勤" name="capture">
        <div class="capture-grid">
          <section class="panel">
            <div class="panel-head">
              <h2>考勤</h2>
              <span class="status-badge">{{ statusText }}</span>
            </div>

>>>>>>> 98bf8e49 (update)
            <div class="camera-frame">
              <video ref="videoRef" autoplay muted playsinline />
            </div>
            <canvas ref="canvasRef" class="hidden-canvas" />

<<<<<<< HEAD
            <div class="camera-actions">
              <el-button type="primary" @click="startCamera">开启摄像头</el-button>
              <el-button @click="stopCamera">关闭摄像头</el-button>
              <el-button :disabled="!cameraReady || processing" @click="captureFrame('manual')">
                5 帧手动抓拍
              </el-button>
              <el-switch
                v-model="autoMode"
                :disabled="!cameraReady"
                active-text="自动多帧抓拍"
                inactive-text="手动模式"
=======
            <div class="challenge-card">
              <div class="challenge-head">
                <strong>活体验证策略</strong>
                <el-tag :type="challengeModeType">{{ challengeModeLabel }}</el-tag>
              </div>

              <div v-if="challengeModeEnabled && currentChallenge" class="challenge-copy">
                <span>{{ currentChallenge.challenge_action_label }}</span>
                <p>{{ currentChallenge.challenge_prompt }}</p>
                <small>
                  基线 {{ currentChallenge.baseline_frame_count }} 帧，动作
                  {{ currentChallenge.action_frame_count }} 帧
                </small>
              </div>

              <div v-else-if="challengeModeEnabled" class="challenge-placeholder">
                当前为增强模式。点击“开始考勤”后，系统会先进行被动活体检测，再追加随机动作校验。
              </div>

              <div v-else class="challenge-placeholder">
                当前为默认模式。点击“开始考勤”后，系统会直接采集多帧图像并执行被动活体反欺诈检测。
              </div>
            </div>

            <div class="camera-actions">
              <el-button type="primary" @click="startCamera">开启摄像头</el-button>
              <el-button @click="stopCamera">关闭摄像头</el-button>
              <el-button :type="challengeModeEnabled ? 'warning' : 'info'" @click="toggleChallengeMode">
                {{ challengeModeLabel }}
              </el-button>
              <el-button
                type="success"
                :disabled="!cameraReady || processing"
                :loading="processing"
                @click="runAttendance('manual')"
              >
                开始考勤
              </el-button>
              <el-switch
                v-model="autoMode"
                :disabled="!cameraReady || processing"
                active-text="自动考勤"
                inactive-text="手动考勤"
>>>>>>> 98bf8e49 (update)
                @change="toggleAutoCapture"
              />
            </div>

            <div class="snapshot-box">
              <span>最近抓拍</span>
              <img v-if="lastSnapshot" :src="lastSnapshot" alt="最近抓拍" />
<<<<<<< HEAD
              <div v-else class="empty-state">连续抓拍完成后将在这里显示最后一帧</div>
=======
              <div v-else class="empty-state">完成一次考勤后，最后一帧会显示在这里。</div>
>>>>>>> 98bf8e49 (update)
            </div>
          </section>

          <section class="panel">
            <div class="panel-head">
              <h2>识别结果</h2>
              <el-tag v-if="result" :type="statusTagType(result.status)">
<<<<<<< HEAD
                {{ result.status }}
=======
                {{ formatStatus(result.status) }}
>>>>>>> 98bf8e49 (update)
              </el-tag>
            </div>

            <div v-if="result" class="result-card">
              <div class="result-grid">
                <div>
                  <span>姓名</span>
                  <strong>{{ result.student_name || "未识别" }}</strong>
                </div>
                <div>
                  <span>学号</span>
                  <strong>{{ result.student_no || "-" }}</strong>
                </div>
                <div>
                  <span>班级</span>
                  <strong>{{ result.class_name || "-" }}</strong>
                </div>
                <div>
                  <span>采集方式</span>
<<<<<<< HEAD
                  <strong>{{ result.capture_mode }}</strong>
=======
                  <strong>{{ formatCaptureMode(result.capture_mode) }}</strong>
                </div>
                <div>
                  <span>验证模式</span>
                  <strong>{{ formatVerificationMode(result.verification_mode) }}</strong>
                </div>
                <div>
                  <span>活体结果</span>
                  <el-tag :type="livenessTagType(result.liveness_result)">
                    {{ formatLivenessResult(result.liveness_result) }}
                  </el-tag>
                </div>
                <div>
                  <span>活体分数</span>
                  <strong>{{ result.liveness_score ?? "-" }}</strong>
                </div>
                <div>
                  <span>模型分数</span>
                  <strong>{{ result.model_score ?? "-" }}</strong>
                </div>
                <div>
                  <span>时序分数</span>
                  <strong>{{ result.heuristic_score ?? "-" }}</strong>
                </div>
                <div>
                  <span>真人帧占比</span>
                  <strong>{{ result.real_frame_ratio ?? "-" }}</strong>
                </div>
                <div>
                  <span>匹配分数</span>
                  <strong>{{ result.match_score ?? "-" }}</strong>
>>>>>>> 98bf8e49 (update)
                </div>
                <div>
                  <span>上传帧数</span>
                  <strong>{{ result.frame_count }}</strong>
                </div>
                <div>
                  <span>有效帧数</span>
                  <strong>{{ result.valid_frame_count }}</strong>
                </div>
                <div>
<<<<<<< HEAD
                  <span>匹配分数</span>
                  <strong>{{ result.match_score }}</strong>
                </div>
                <div>
                  <span>活体结果</span>
                  <el-tag :type="livenessTagType(result.liveness_result)">
                    {{ result.liveness_result }}
                  </el-tag>
                </div>
                <div>
                  <span>活体模式</span>
                  <strong>{{ result.liveness_mode }}</strong>
                </div>
                <div>
                  <span>活体分数</span>
                  <strong>{{ result.liveness_score }}</strong>
                </div>
                <div>
                  <span>记录ID</span>
                  <strong>{{ result.record_id }}</strong>
                </div>
=======
                  <span>随机动作结果</span>
                  <el-tag :type="challengeTagType(result.challenge_result)">
                    {{ formatChallengeResult(result.challenge_result) }}
                  </el-tag>
                </div>
                <div>
                  <span>随机动作分数</span>
                  <strong>{{ result.challenge_score ?? "-" }}</strong>
                </div>
                <div>
                  <span>反欺诈类型</span>
                  <strong>{{ result.spoof_attack_type || "-" }}</strong>
                </div>
                <div>
                  <span>静态分数</span>
                  <strong>{{ result.static_score ?? "-" }}</strong>
                </div>
                <div>
                  <span>情绪</span>
                  <strong>{{ formatEmotion(result.emotion) }}</strong>
                </div>
                <div>
                  <span>记录 ID</span>
                  <strong>{{ result.record_id || "-" }}</strong>
                </div>
              </div>
              <div class="panel-tip" v-if="result.challenge_prompt">
                挑战提示：{{ result.challenge_prompt }}
              </div>
              <div class="panel-tip" v-if="result.reason">
                {{ result.reason }}
>>>>>>> 98bf8e49 (update)
              </div>
            </div>

            <div v-else class="empty-card">
<<<<<<< HEAD
              开启摄像头后，系统会一次采集 5 帧做时序活体检测，再进行识别。
            </div>

            <div class="panel-tip">
              多帧活体检测更依赖连续变化。演示时建议保持正视镜头，并轻微眨眼或缓慢转头。
=======
              默认使用被动活体检测；如需更严格验证，可先开启“随机动作增强”再开始考勤。
>>>>>>> 98bf8e49 (update)
            </div>
          </section>
        </div>
      </el-tab-pane>

      <el-tab-pane label="考勤记录" name="records">
        <section class="panel">
          <div class="panel-head">
<<<<<<< HEAD
            <h2>筛选与导出</h2>
=======
            <h2>考勤记录</h2>
>>>>>>> 98bf8e49 (update)
            <div class="record-actions">
              <el-button @click="resetFilters">重置筛选</el-button>
              <el-button type="primary" @click="loadRecords">查询</el-button>
              <el-button type="success" @click="downloadRecords">导出 Excel</el-button>
            </div>
          </div>

          <el-form class="filters-form" label-position="top">
            <div class="filters-grid">
              <el-form-item label="姓名/学号">
                <el-input v-model="filters.keyword" placeholder="模糊搜索" />
              </el-form-item>
              <el-form-item label="班级">
                <el-input v-model="filters.class_name" placeholder="如：信安1班" />
              </el-form-item>
              <el-form-item label="考勤状态">
                <el-select v-model="filters.status" clearable placeholder="全部">
                  <el-option label="成功" value="present" />
                  <el-option label="未匹配" value="unknown" />
<<<<<<< HEAD
                  <el-option label="活体拒绝" value="rejected" />
=======
                  <el-option label="拒绝" value="rejected" />
>>>>>>> 98bf8e49 (update)
                </el-select>
              </el-form-item>
              <el-form-item label="采集方式">
                <el-select v-model="filters.capture_mode" clearable placeholder="全部">
<<<<<<< HEAD
                  <el-option label="手动抓拍" value="manual" />
                  <el-option label="自动抓拍" value="auto" />
=======
                  <el-option label="手动" value="manual" />
                  <el-option label="自动" value="auto" />
>>>>>>> 98bf8e49 (update)
                </el-select>
              </el-form-item>
              <el-form-item label="活体结果">
                <el-select v-model="filters.liveness_result" clearable placeholder="全部">
<<<<<<< HEAD
                  <el-option label="真实" value="real" />
                  <el-option label="伪造" value="fake" />
=======
                  <el-option label="真人" value="real" />
                  <el-option label="未通过" value="fake" />
                  <el-option label="待重试" value="uncertain" />
>>>>>>> 98bf8e49 (update)
                </el-select>
              </el-form-item>
              <el-form-item label="开始日期">
                <el-date-picker
                  v-model="filters.start_date"
                  type="date"
                  value-format="YYYY-MM-DD"
                  placeholder="开始日期"
                />
              </el-form-item>
              <el-form-item label="结束日期">
                <el-date-picker
                  v-model="filters.end_date"
                  type="date"
                  value-format="YYYY-MM-DD"
                  placeholder="结束日期"
                />
              </el-form-item>
            </div>
          </el-form>

          <el-table :data="records" v-loading="loadingRecords" border stripe>
            <el-table-column prop="id" label="ID" width="70" />
            <el-table-column prop="student_no" label="学号" width="120" />
            <el-table-column prop="student_name" label="姓名" width="110" />
            <el-table-column prop="class_name" label="班级" width="130" />
<<<<<<< HEAD
            <el-table-column label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="statusTagType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="capture_mode" label="采集方式" width="100" />
            <el-table-column prop="frame_count" label="上传帧数" width="100" />
            <el-table-column prop="valid_frame_count" label="有效帧数" width="100" />
            <el-table-column label="活体结果" width="110">
              <template #default="{ row }">
                <el-tag
                  v-if="row.liveness_result"
                  :type="livenessTagType(row.liveness_result)"
                >
                  {{ row.liveness_result }}
                </el-tag>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column prop="liveness_mode" label="活体模式" width="160" />
            <el-table-column prop="liveness_score" label="活体分数" width="110" />
            <el-table-column prop="match_score" label="匹配分数" width="110" />
            <el-table-column prop="created_at" label="考勤时间" min-width="180" />
            <el-table-column prop="note" label="备注" min-width="220" />
=======
            <el-table-column label="状态" width="110">
              <template #default="{ row }">
                <el-tag :type="statusTagType(row.status)">{{ formatStatus(row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="采集方式" width="100">
              <template #default="{ row }">
                {{ formatCaptureMode(row.capture_mode) }}
              </template>
            </el-table-column>
            <el-table-column label="验证模式" min-width="150">
              <template #default="{ row }">
                {{ formatVerificationMode(row.verification_mode) }}
              </template>
            </el-table-column>
            <el-table-column label="活体结果" width="110">
              <template #default="{ row }">
                <el-tag :type="livenessTagType(row.liveness_result)">
                  {{ formatLivenessResult(row.liveness_result) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="随机动作结果" width="120">
              <template #default="{ row }">
                <el-tag :type="challengeTagType(row.challenge_result)">
                  {{ formatChallengeResult(row.challenge_result) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="challenge_action_label" label="随机动作" width="120" />
            <el-table-column prop="match_score" label="匹配分数" width="110" />
            <el-table-column prop="created_at" label="考勤时间" min-width="170" />
            <el-table-column prop="note" label="备注" min-width="240" show-overflow-tooltip />
>>>>>>> 98bf8e49 (update)
          </el-table>
        </section>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>
<<<<<<< HEAD
=======

<style scoped>
.challenge-card {
  margin-top: 18px;
  padding: 16px 18px;
  border-radius: 22px;
  border: 1px solid var(--line);
  background: rgba(255, 250, 244, 0.74);
}

.challenge-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.challenge-card strong {
  display: block;
  margin-bottom: 8px;
}

.challenge-copy span {
  display: block;
  font-weight: 700;
}

.challenge-copy p,
.challenge-placeholder {
  margin: 8px 0;
  color: var(--muted);
  line-height: 1.7;
}

.challenge-copy small {
  color: var(--muted);
}
</style>
>>>>>>> 98bf8e49 (update)
