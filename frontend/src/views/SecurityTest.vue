<script setup>
import { computed, onBeforeUnmount, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

<<<<<<< HEAD
=======
import { createLivenessChallenge } from "../api/liveness";
>>>>>>> 98bf8e49 (update)
import {
  exportSecurityTestRecords,
  fetchSecurityTestRecords,
  fetchSecurityTestSummary,
  runSecurityLivenessTest,
} from "../api/securityTests";
import TeacherHeader from "../components/TeacherHeader.vue";
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();
const videoRef = ref(null);
const canvasRef = ref(null);
const streamRef = ref(null);

const user = ref(null);
const cameraReady = ref(false);
const processing = ref(false);
const loadingRecords = ref(false);
const exporting = ref(false);
<<<<<<< HEAD
const statusText = ref("等待开启摄像头");
const result = ref(null);
const records = ref([]);
const uploadFiles = ref([]);
=======
const challengeModeEnabled = ref(false);
const statusText = ref("等待开启摄像头");
const result = ref(null);
const records = ref([]);
const currentChallenge = ref(null);
>>>>>>> 98bf8e49 (update)
const summary = ref({
  dashboard: {},
  test_type_distribution: [],
  result_distribution: [],
  mode_distribution: [],
<<<<<<< HEAD
=======
  action_distribution: [],
  attack_distribution: [],
>>>>>>> 98bf8e49 (update)
  type_breakdown: [],
  daily_trend: [],
});

<<<<<<< HEAD
const BURST_FRAME_COUNT = 5;
const BURST_INTERVAL_MS = 220;

const uploadForm = reactive({
  testType: "photo_attack",
=======
const FRAME_INTERVAL_MS = 220;
const ACTION_READY_DELAY_MS = 900;
const PASSIVE_FRAME_COUNT = 5;

const testForm = reactive({
  testType: "real_person",
>>>>>>> 98bf8e49 (update)
  remark: "",
});

const filters = reactive({
  keyword: "",
  test_type: "",
  result: "",
  liveness_mode: "",
  operator_username: "",
  start_date: "",
  end_date: "",
});

const typeLabelMap = {
<<<<<<< HEAD
  live_sample: "实时活体",
  photo_attack: "照片攻击",
  video_attack: "视频攻击",
=======
  real_person: "真人",
  printed_photo: "打印照片",
  screen_photo: "屏幕照片",
  screen_video: "屏幕视频",
>>>>>>> 98bf8e49 (update)
};

const resultLabelMap = {
  real: "通过",
<<<<<<< HEAD
  fake: "拦截",
=======
  fake: "未通过",
  uncertain: "待重试",
};

const challengeResultLabelMap = {
  passed: "通过",
  failed: "未通过",
  uncertain: "待重试",
  skipped: "未启用",
};

const challengeActionLabelMap = {
  turn_left: "向左转头",
  turn_right: "向右转头",
  nod_down: "低头",
>>>>>>> 98bf8e49 (update)
};

const maxTypeCount = computed(() => {
  const counts = summary.value.test_type_distribution.map((item) => item.count);
  return counts.length ? Math.max(...counts) : 1;
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

function formatTestType(value) {
  return typeLabelMap[value] || value || "-";
}

function formatResult(value) {
  return resultLabelMap[value] || value || "-";
}

<<<<<<< HEAD
function resultTagType(value) {
  return value === "real" ? "success" : "danger";
=======
function formatChallengeResult(value) {
  return challengeResultLabelMap[value] || value || "-";
}

function formatChallengeAction(value, label) {
  return label || challengeActionLabelMap[value] || value || "-";
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

function resultTagType(value) {
  if (value === "real") return "success";
  if (value === "uncertain") return "warning";
  return "danger";
}

function challengeTagType(value) {
  if (value === "passed") return "success";
  if (value === "uncertain") return "warning";
  if (value === "skipped") return "info";
  return "danger";
>>>>>>> 98bf8e49 (update)
}

function typeWidth(count) {
  return `${Math.max((count / maxTypeCount.value) * 100, 8)}%`;
}

function buildQuery() {
  return {
    keyword: filters.keyword || undefined,
    test_type: filters.test_type || undefined,
    result: filters.result || undefined,
    liveness_mode: filters.liveness_mode || undefined,
    operator_username: filters.operator_username || undefined,
    start_date: filters.start_date || undefined,
    end_date: filters.end_date || undefined,
  };
}

function stopCamera() {
  const stream = streamRef.value;
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
  }
  streamRef.value = null;
  cameraReady.value = false;
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
    setStatus("摄像头已开启，可进行实时活体安全测试");
=======
    setStatus(
      challengeModeEnabled.value
        ? "摄像头已开启，可开始安全测试。当前为被动活体 + 随机动作增强模式"
        : "摄像头已开启，可开始安全测试。当前为默认被动活体模式",
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
=======
async function captureFrames(count) {
>>>>>>> 98bf8e49 (update)
  const video = videoRef.value;
  const canvas = canvasRef.value;
  if (!video || !canvas) {
    throw new Error("视频组件尚未准备完成");
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
    const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
    blobs.push(blob);
    if (index < BURST_FRAME_COUNT - 1) {
      await sleep(BURST_INTERVAL_MS);
    }
  }
=======
  for (let index = 0; index < count; index += 1) {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
    if (!blob) {
      throw new Error("截图失败，请重试");
    }
    blobs.push(blob);
    if (index < count - 1) {
      await sleep(FRAME_INTERVAL_MS);
    }
  }

>>>>>>> 98bf8e49 (update)
  return blobs;
}

async function loadRecords() {
  loadingRecords.value = true;
  try {
    const response = await fetchSecurityTestRecords(buildQuery());
    records.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "安全测试记录加载失败");
  } finally {
    loadingRecords.value = false;
  }
}

async function loadSummary() {
  try {
    const response = await fetchSecurityTestSummary(buildQuery());
<<<<<<< HEAD
    summary.value = response.data;
=======
    summary.value = {
      action_distribution: [],
      attack_distribution: [],
      ...response.data,
    };
>>>>>>> 98bf8e49 (update)
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "安全测试统计加载失败");
  }
}

async function refreshAll() {
  await Promise.all([loadRecords(), loadSummary()]);
}

function resetFilters() {
  filters.keyword = "";
  filters.test_type = "";
  filters.result = "";
  filters.liveness_mode = "";
  filters.operator_username = "";
  filters.start_date = "";
  filters.end_date = "";
  refreshAll();
}

<<<<<<< HEAD
=======
async function requestChallenge() {
  const response = await createLivenessChallenge({ purpose: "security_test" });
  currentChallenge.value = response.data;
  return response.data;
}

function toggleChallengeMode() {
  challengeModeEnabled.value = !challengeModeEnabled.value;
  currentChallenge.value = null;
  setStatus(
    challengeModeEnabled.value
      ? "已开启随机动作增强。开始测试后会先做被动活体，再叠加随机动作校验"
      : "已关闭随机动作增强。开始测试后将直接做默认被动活体检测",
  );
}

>>>>>>> 98bf8e49 (update)
async function runLiveTest() {
  if (!cameraReady.value || processing.value) {
    return;
  }
<<<<<<< HEAD
  processing.value = true;
  setStatus(`正在采集 ${BURST_FRAME_COUNT} 帧进行实时活体测试`);
  try {
    const blobs = await captureBurstBlobs();
    const response = await runSecurityLivenessTest({
      blobs,
      testType: "live_sample",
      remark: "摄像头实时活体验证",
    });
    result.value = response.data;
    setStatus(`实时测试完成，结果：${formatResult(response.data.result)}`);
    ElMessage.success(`实时测试完成：${formatResult(response.data.result)}`);
=======

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
      const actionBlobs = await captureFrames(actionCount);

      blobs = [...baselineBlobs, ...actionBlobs];
      challengeId = challenge.challenge_id;
    } else {
      currentChallenge.value = null;
      setStatus("正在采集 5 帧图像并执行多帧被动活体检测");
      blobs = await captureFrames(PASSIVE_FRAME_COUNT);
    }

    const response = await runSecurityLivenessTest({
      blobs,
      testType: testForm.testType,
      remark: testForm.remark,
      challengeId,
    });
    result.value = response.data;

    const message =
      response.data.challenge_reason ||
      response.data.reason ||
      `实时测试完成：${formatResult(response.data.result)}`;
    setStatus(message);
    if (response.data.result === "real") {
      ElMessage.success(message);
    } else if (response.data.result === "uncertain") {
      ElMessage.warning(message);
    } else {
      ElMessage.error(message);
    }

>>>>>>> 98bf8e49 (update)
    await refreshAll();
  } catch (error) {
    const message = error.response?.data?.message || error.message || "实时安全测试失败";
    setStatus(message);
    ElMessage.error(message);
  } finally {
    processing.value = false;
  }
}

<<<<<<< HEAD
function handleUploadChange(uploadFile, uploadFileList) {
  uploadFiles.value = uploadFileList.map((item) => item.raw).filter(Boolean);
}

async function runUploadTest() {
  if (!uploadFiles.value.length || processing.value) {
    ElMessage.warning("请先选择测试图片");
    return;
  }
  processing.value = true;
  setStatus("正在上传样本并执行多帧活体检测");
  try {
    const response = await runSecurityLivenessTest({
      blobs: uploadFiles.value,
      testType: uploadForm.testType,
      remark: uploadForm.remark,
    });
    result.value = response.data;
    setStatus(`样本测试完成，结果：${formatResult(response.data.result)}`);
    ElMessage.success(`样本测试完成：${formatResult(response.data.result)}`);
    await refreshAll();
  } catch (error) {
    const message = error.response?.data?.message || "样本安全测试失败";
    setStatus(message);
    ElMessage.error(message);
  } finally {
    processing.value = false;
  }
}

=======
>>>>>>> 98bf8e49 (update)
async function downloadRecords() {
  exporting.value = true;
  try {
    const response = await exportSecurityTestRecords(buildQuery());
    const blob = new Blob([response.data], {
      type: response.headers["content-type"],
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    const disposition = response.headers["content-disposition"] || "";
<<<<<<< HEAD
    const match = disposition.match(/filename=\"?([^\"]+)\"?/);
=======
    const match = disposition.match(/filename="?([^"]+)"?/);
>>>>>>> 98bf8e49 (update)
    link.href = url;
    link.download = match?.[1] || "security_test_report.xlsx";
    link.click();
    window.URL.revokeObjectURL(url);
    ElMessage.success("安全测试记录导出成功");
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "安全测试记录导出失败");
  } finally {
    exporting.value = false;
  }
}

async function logout() {
  stopCamera();
  await performLogout(router);
}

<<<<<<< HEAD
function openAttendancePage() {
  router.push({ name: "attendance" });
}

function openStudentsPage() {
  router.push({ name: "students" });
}

function openGroupPhotosPage() {
  router.push({ name: "group-photos" });
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

function openEmotionPage() {
  router.push({ name: "emotions" });
}

function openReportPage() {
  router.push({ name: "report" });
}

=======
>>>>>>> 98bf8e49 (update)
onMounted(async () => {
  user.value = parseSavedUser();
  await refreshAll();
});

onBeforeUnmount(() => {
  stopCamera();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="安全测试" current="security-tests" :user="user" @logout="logout" />

    <section class="stats-grid">
      <article class="stat-card">
        <span>测试总数</span>
        <strong>{{ summary.dashboard.total_count || 0 }}</strong>
      </article>
      <article class="stat-card success">
        <span>通过次数</span>
        <strong>{{ summary.dashboard.real_count || 0 }}</strong>
      </article>
      <article class="stat-card danger">
<<<<<<< HEAD
        <span>拦截次数</span>
        <strong>{{ summary.dashboard.fake_count || 0 }}</strong>
      </article>
      <article class="stat-card warning">
=======
        <span>未通过次数</span>
        <strong>{{ summary.dashboard.fake_count || 0 }}</strong>
      </article>
      <article class="stat-card warning">
        <span>待重试</span>
        <strong>{{ summary.dashboard.uncertain_count || 0 }}</strong>
      </article>
      <article class="stat-card">
>>>>>>> 98bf8e49 (update)
        <span>今日测试</span>
        <strong>{{ summary.dashboard.today_count || 0 }}</strong>
      </article>
    </section>

    <div class="capture-grid">
      <section class="panel">
        <div class="panel-head">
<<<<<<< HEAD
          <h2>实时活体验证</h2>
          <span class="status-badge">{{ statusText }}</span>
        </div>
=======
          <h2>安全测试</h2>
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
          <el-button :disabled="!cameraReady || processing" @click="runLiveTest">
            实时 5 帧检测
          </el-button>
        </div>
        <div class="panel-tip">
          这里用于演示真实用户的多帧活体检测。建议在镜头前轻微眨眼或缓慢转头。
=======

        <el-form label-position="top" class="security-form">
          <div class="filters-grid">
            <el-form-item label="测试场景">
              <el-select v-model="testForm.testType">
                <el-option label="真人" value="real_person" />
                <el-option label="打印照片" value="printed_photo" />
                <el-option label="屏幕照片" value="screen_photo" />
                <el-option label="屏幕视频" value="screen_video" />
              </el-select>
            </el-form-item>
            <el-form-item label="备注">
              <el-input v-model="testForm.remark" placeholder="如：手机播放录播视频" />
            </el-form-item>
          </div>
        </el-form>

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
            当前为增强模式。点击“开始测试”后，系统会先进行被动活体检测，再追加随机动作校验。
          </div>

          <div v-else class="challenge-placeholder">
            当前为默认模式。点击“开始测试”后，系统会直接采集多帧图像并执行被动活体反欺诈检测。
          </div>
        </div>

        <div class="camera-actions">
          <el-button type="primary" @click="startCamera">开启摄像头</el-button>
          <el-button @click="stopCamera">关闭摄像头</el-button>
          <el-button :type="challengeModeEnabled ? 'warning' : 'info'" @click="toggleChallengeMode">
            {{ challengeModeLabel }}
          </el-button>
          <el-button type="success" :disabled="!cameraReady || processing" :loading="processing" @click="runLiveTest">
            开始测试
          </el-button>
>>>>>>> 98bf8e49 (update)
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
<<<<<<< HEAD
          <h2>攻击样本测试</h2>
        </div>
        <el-form label-position="top">
          <div class="filters-grid">
            <el-form-item label="测试类型">
              <el-select v-model="uploadForm.testType">
                <el-option label="照片攻击" value="photo_attack" />
                <el-option label="视频攻击" value="video_attack" />
              </el-select>
            </el-form-item>
            <el-form-item label="备注">
              <el-input v-model="uploadForm.remark" placeholder="如：打印照片攻击样本" />
            </el-form-item>
          </div>
          <el-form-item label="上传测试帧">
            <el-upload
              drag
              multiple
              :auto-upload="false"
              :show-file-list="true"
              :on-change="handleUploadChange"
              :limit="8"
            >
              <div class="upload-placeholder">
                上传 1-8 张图片。若要模拟视频攻击，建议上传连续截图。
              </div>
            </el-upload>
          </el-form-item>
          <el-button type="danger" :loading="processing" @click="runUploadTest">
            运行样本测试
          </el-button>
        </el-form>
=======
          <h2>最近一次结果</h2>
          <el-tag v-if="result" :type="resultTagType(result.result)">
            {{ formatResult(result.result) }}
          </el-tag>
        </div>

        <div v-if="result" class="result-card">
          <div class="result-grid">
            <div>
              <span>测试场景</span>
              <strong>{{ formatTestType(result.test_type) }}</strong>
            </div>
            <div>
              <span>测试结果</span>
              <strong>{{ formatResult(result.result) }}</strong>
            </div>
            <div>
              <span>验证模式</span>
              <strong>{{ formatVerificationMode(result.verification_mode) }}</strong>
            </div>
            <div>
              <span>活体分数</span>
              <strong>{{ result.liveness_score ?? result.score ?? "-" }}</strong>
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
              <span>上传帧数</span>
              <strong>{{ result.frame_count }}</strong>
            </div>
            <div>
              <span>有效帧数</span>
              <strong>{{ result.valid_frame_count }}</strong>
            </div>
            <div>
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
              <span>操作人</span>
              <strong>{{ user?.username || "-" }}</strong>
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
          </div>
        </div>

        <div v-else class="empty-card">
          默认使用被动活体检测；如需更严格测试，可先开启“随机动作增强”再开始测试。
        </div>
>>>>>>> 98bf8e49 (update)
      </section>
    </div>

    <div class="capture-grid security-panel-gap">
      <section class="panel">
        <div class="panel-head">
          <h2>测试类型分布</h2>
        </div>
        <div class="bar-list">
<<<<<<< HEAD
          <div
            v-for="item in summary.test_type_distribution"
            :key="item.test_type"
            class="bar-row"
          >
=======
          <div v-for="item in summary.test_type_distribution" :key="item.test_type" class="bar-row">
>>>>>>> 98bf8e49 (update)
            <div class="bar-label">
              <strong>{{ formatTestType(item.test_type) }}</strong>
              <span>{{ item.test_type }}</span>
            </div>
            <div class="bar-track">
              <div class="bar-fill secondary" :style="{ width: typeWidth(item.count) }"></div>
            </div>
            <div class="bar-value">{{ item.count }}</div>
          </div>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
<<<<<<< HEAD
          <h2>结果与阈值概览</h2>
=======
          <h2>结果概览</h2>
>>>>>>> 98bf8e49 (update)
        </div>
        <div class="chip-grid">
          <article v-for="item in summary.result_distribution" :key="item.result" class="chip-card">
            <span>{{ formatResult(item.result) }}</span>
            <strong>{{ item.count }}</strong>
          </article>
        </div>
<<<<<<< HEAD
        <div class="result-card security-summary-card">
          <div class="result-grid">
            <div>
              <span>平均活体分数</span>
=======
        <div class="chip-grid security-chip-grid">
          <article
            v-for="item in summary.mode_distribution"
            :key="item.verification_mode"
            class="chip-card"
          >
            <span>{{ formatVerificationMode(item.verification_mode) }}</span>
            <strong>{{ item.count }}</strong>
          </article>
        </div>
        <div class="result-card security-summary-card">
          <div class="result-grid">
            <div>
              <span>平均分数</span>
>>>>>>> 98bf8e49 (update)
              <strong>{{ summary.dashboard.average_score || 0 }}</strong>
            </div>
            <div>
              <span>平均置信度</span>
              <strong>{{ summary.dashboard.average_confidence || 0 }}</strong>
            </div>
          </div>
        </div>
      </section>
    </div>

    <section class="panel security-panel-gap">
      <div class="panel-head">
<<<<<<< HEAD
        <h2>最近一次测试结果</h2>
        <el-tag v-if="result" :type="resultTagType(result.result)">
          {{ formatResult(result.result) }}
        </el-tag>
      </div>
      <div v-if="result" class="result-card">
        <div class="result-grid">
          <div>
            <span>测试类型</span>
            <strong>{{ formatTestType(result.test_type) }}</strong>
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
            <span>结果</span>
            <strong>{{ formatResult(result.result) }}</strong>
          </div>
          <div>
            <span>活体分数</span>
            <strong>{{ result.score }}</strong>
          </div>
          <div>
            <span>置信度</span>
            <strong>{{ result.confidence }}</strong>
          </div>
          <div>
            <span>活体模式</span>
            <strong>{{ result.liveness_mode }}</strong>
          </div>
          <div>
            <span>时间变化强度</span>
            <strong>{{ result.temporal?.texture_diff ?? "-" }}</strong>
          </div>
        </div>
      </div>
      <div v-else class="empty-card">运行一次实时测试或上传样本后，结果会显示在这里。</div>
    </section>

    <section class="panel security-panel-gap">
      <div class="panel-head">
=======
>>>>>>> 98bf8e49 (update)
        <h2>安全测试记录</h2>
        <div class="record-actions">
          <el-button @click="resetFilters">重置筛选</el-button>
          <el-button type="primary" @click="refreshAll">查询</el-button>
          <el-button type="success" :loading="exporting" @click="downloadRecords">
            导出 Excel
          </el-button>
        </div>
      </div>

      <el-form class="filters-form" label-position="top">
        <div class="filters-grid">
<<<<<<< HEAD
          <el-form-item label="关键词">
            <el-input v-model="filters.keyword" placeholder="按备注、模式、操作人搜索" />
          </el-form-item>
          <el-form-item label="测试类型">
            <el-select v-model="filters.test_type" clearable placeholder="全部">
              <el-option label="实时活体" value="live_sample" />
              <el-option label="照片攻击" value="photo_attack" />
              <el-option label="视频攻击" value="video_attack" />
=======
          <el-form-item label="关键字">
            <el-input v-model="filters.keyword" placeholder="按备注、操作人搜索" />
          </el-form-item>
          <el-form-item label="测试类型">
            <el-select v-model="filters.test_type" clearable placeholder="全部">
              <el-option label="真人" value="real_person" />
              <el-option label="打印照片" value="printed_photo" />
              <el-option label="屏幕照片" value="screen_photo" />
              <el-option label="屏幕视频" value="screen_video" />
>>>>>>> 98bf8e49 (update)
            </el-select>
          </el-form-item>
          <el-form-item label="结果">
            <el-select v-model="filters.result" clearable placeholder="全部">
              <el-option label="通过" value="real" />
<<<<<<< HEAD
              <el-option label="拦截" value="fake" />
            </el-select>
          </el-form-item>
          <el-form-item label="活体模式">
            <el-input v-model="filters.liveness_mode" placeholder="如：temporal_texture" />
=======
              <el-option label="未通过" value="fake" />
              <el-option label="待重试" value="uncertain" />
            </el-select>
          </el-form-item>
          <el-form-item label="活体模式">
            <el-select v-model="filters.liveness_mode" clearable placeholder="全部">
              <el-option label="被动活体" value="passive_anti_spoof" />
              <el-option label="被动活体 + 随机动作" value="passive_plus_challenge" />
            </el-select>
>>>>>>> 98bf8e49 (update)
          </el-form-item>
          <el-form-item label="操作人">
            <el-input v-model="filters.operator_username" placeholder="如：teacher" />
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
<<<<<<< HEAD
        <el-table-column label="测试类型" width="120">
=======
        <el-table-column label="测试类型" width="130">
>>>>>>> 98bf8e49 (update)
          <template #default="{ row }">
            <span>{{ formatTestType(row.test_type) }}</span>
          </template>
        </el-table-column>
<<<<<<< HEAD
        <el-table-column prop="frame_count" label="上传帧数" width="100" />
        <el-table-column prop="valid_frame_count" label="有效帧数" width="100" />
=======
>>>>>>> 98bf8e49 (update)
        <el-table-column label="结果" width="100">
          <template #default="{ row }">
            <el-tag :type="resultTagType(row.result)">{{ formatResult(row.result) }}</el-tag>
          </template>
        </el-table-column>
<<<<<<< HEAD
        <el-table-column prop="score" label="活体分数" width="110" />
        <el-table-column prop="confidence" label="置信度" width="110" />
        <el-table-column prop="threshold" label="阈值" width="90" />
        <el-table-column prop="liveness_mode" label="活体模式" min-width="160" />
=======
        <el-table-column label="验证模式" min-width="150">
          <template #default="{ row }">
            {{ formatVerificationMode(row.verification_mode) }}
          </template>
        </el-table-column>
        <el-table-column label="随机动作" width="120">
          <template #default="{ row }">
            {{ formatChallengeAction(row.challenge_action, row.challenge_action_label) }}
          </template>
        </el-table-column>
        <el-table-column label="随机动作结果" width="120">
          <template #default="{ row }">
            <el-tag :type="challengeTagType(row.challenge_result)">
              {{ formatChallengeResult(row.challenge_result) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="spoof_attack_type" label="反欺诈类型" width="140" />
>>>>>>> 98bf8e49 (update)
        <el-table-column prop="operator_username" label="操作人" width="120" />
        <el-table-column prop="remark" label="备注" min-width="180" show-overflow-tooltip />
        <el-table-column prop="created_at" label="测试时间" min-width="170" />
      </el-table>
    </section>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>按测试类型汇总</h2>
      </div>
      <el-table :data="summary.type_breakdown" border stripe>
        <el-table-column label="测试类型" min-width="130">
          <template #default="{ row }">
            <span>{{ row.label }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="count" label="总次数" width="90" />
        <el-table-column prop="real_count" label="通过次数" width="100" />
<<<<<<< HEAD
        <el-table-column prop="fake_count" label="拦截次数" width="100" />
        <el-table-column prop="average_score" label="平均活体分数" width="130" />
=======
        <el-table-column prop="fake_count" label="未通过次数" width="110" />
        <el-table-column prop="average_score" label="平均分数" width="140" />
>>>>>>> 98bf8e49 (update)
      </el-table>
    </section>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>每日测试趋势</h2>
      </div>
      <el-table :data="summary.daily_trend" border stripe>
        <el-table-column prop="date" label="日期" width="120" />
        <el-table-column prop="real" label="通过" width="90" />
<<<<<<< HEAD
        <el-table-column prop="fake" label="拦截" width="90" />
=======
        <el-table-column prop="fake" label="未通过" width="90" />
        <el-table-column prop="uncertain" label="待重试" width="90" />
>>>>>>> 98bf8e49 (update)
        <el-table-column prop="total" label="总数" width="90" />
      </el-table>
    </section>
  </div>
</template>

<style scoped>
<<<<<<< HEAD
.security-summary-card {
  margin-top: 18px;
}
=======
.security-form,
.security-summary-card {
  margin-top: 18px;
}

.security-chip-grid,
.security-panel-gap {
  margin-top: 16px;
}

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
>>>>>>> 98bf8e49 (update)
</style>
