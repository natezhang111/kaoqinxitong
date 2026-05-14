<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import TeacherHeader from "../components/TeacherHeader.vue";
import {
  fetchModelStatus,
  fetchSystemHealth,
  fetchSystemSummary,
} from "../api/system";
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();

const user = ref(null);
const loading = ref(false);
const health = ref(null);
const summary = ref({
  user_count: 0,
  student_count: 0,
  attendance_count: 0,
});
const modelStatus = ref({
  device: "unknown",
  models: {},
  face_engine: {},
  liveness_engine: {},
  emotion_engine: {},
});

const summaryCards = computed(() => [
  {
    key: "status",
    label: "服务状态",
    value: health.value?.status || "-",
    tone: health.value?.status === "ok" ? "success" : "danger",
  },
  {
    key: "device",
    label: "推理设备",
    value: modelStatus.value.device || "unknown",
    tone: "primary",
  },
  {
    key: "users",
    label: "系统用户数",
    value: summary.value.user_count || 0,
    tone: "primary",
  },
  {
    key: "students",
    label: "学生档案数",
    value: summary.value.student_count || 0,
    tone: "success",
  },
  {
    key: "attendance",
    label: "考勤记录数",
    value: summary.value.attendance_count || 0,
    tone: "warning",
  },
]);

const modelRows = computed(() =>
  Object.entries(modelStatus.value.models || {}).map(([name, status]) => ({
    name,
    status,
  }))
);

const engineRows = computed(() => [
  { name: "face_engine", detail: modelStatus.value.face_engine || {} },
  { name: "liveness_engine", detail: modelStatus.value.liveness_engine || {} },
  { name: "emotion_engine", detail: modelStatus.value.emotion_engine || {} },
]);

function statusTagType(value) {
  if (value === "ok" || value === "ready") return "success";
  if (value === "not_initialized") return "warning";
  return "info";
}

async function loadStatus() {
  loading.value = true;
  try {
    const [healthResponse, summaryResponse, modelResponse] = await Promise.all([
      fetchSystemHealth(),
      fetchSystemSummary(),
      fetchModelStatus(),
    ]);
    health.value = healthResponse.data;
    summary.value = summaryResponse.data;
    modelStatus.value = modelResponse.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "系统状态加载失败");
  } finally {
    loading.value = false;
  }
}

async function logout() {
  await performLogout(router);
}

function goToAttendance() {
  router.push({ name: "attendance" });
}

function goToStudents() {
  router.push({ name: "students" });
}

function goToSecurityTests() {
  router.push({ name: "security-tests" });
}

function goToGroupPhotos() {
  router.push({ name: "group-photos" });
}

function goToEmotions() {
  router.push({ name: "emotions" });
}

function goToReport() {
  router.push({ name: "report" });
}

function goToUsers() {
  router.push({ name: "users" });
}

function goToAuditLogs() {
  router.push({ name: "audit-logs" });
}

function goToTeacherProfile() {
  router.push({ name: "teacher-profile" });
}

onMounted(async () => {
  user.value = parseSavedUser();
  await loadStatus();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="系统状态" current="system-status" :user="user" @logout="logout" />

    <section class="stats-grid" v-loading="loading">
      <article
        v-for="item in summaryCards"
        :key="item.key"
        class="stat-card"
        :class="`tone-${item.tone}`"
      >
        <span>{{ item.label }}</span>
        <strong>{{ item.value }}</strong>
      </article>
    </section>

    <div class="panel-grid">
      <section class="panel" v-loading="loading">
        <div class="panel-head">
          <h2>服务健康检查</h2>
          <el-button @click="loadStatus">刷新状态</el-button>
        </div>
        <div class="info-grid">
          <article class="info-item">
            <span>应用名称</span>
            <strong>{{ health?.app_name || "-" }}</strong>
          </article>
          <article class="info-item">
            <span>版本</span>
            <strong>{{ health?.version || "-" }}</strong>
          </article>
          <article class="info-item">
            <span>服务状态</span>
            <el-tag :type="statusTagType(health?.status)">
              {{ health?.status || "-" }}
            </el-tag>
          </article>
          <article class="info-item">
            <span>服务器时间</span>
            <strong>{{ health?.server_time || "-" }}</strong>
          </article>
        </div>
      </section>

      <section class="panel" v-loading="loading">
        <div class="panel-head">
          <h2>模型状态</h2>
        </div>
        <el-table :data="modelRows" border stripe>
          <el-table-column prop="name" label="模型项" min-width="180" />
          <el-table-column label="状态" width="140">
            <template #default="{ row }">
              <el-tag :type="statusTagType(row.status)">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </section>
    </div>

    <section class="panel" v-loading="loading">
      <div class="panel-head">
        <h2>引擎详情</h2>
      </div>
      <div class="engine-grid">
        <article v-for="item in engineRows" :key="item.name" class="engine-card">
          <h3>{{ item.name }}</h3>
          <pre>{{ JSON.stringify(item.detail, null, 2) }}</pre>
        </article>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-shell {
  min-height: 100vh;
  padding: 24px;
  background:
    radial-gradient(circle at top left, rgba(14, 165, 233, 0.14), transparent 28%),
    radial-gradient(circle at right, rgba(34, 197, 94, 0.12), transparent 20%),
    #f4f7fb;
}

.topbar {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 24px 28px;
  margin-bottom: 20px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
}

.eyebrow {
  margin: 0 0 8px;
  color: #0891b2;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.topbar h1 {
  margin: 0;
  font-size: 30px;
}

.subcopy {
  margin: 10px 0 0;
  color: #475569;
}

.topbar-actions {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.nav-switcher {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
}

.user-pill {
  min-width: 120px;
  padding: 10px 14px;
  border-radius: 16px;
  background: #ecfeff;
  color: #0f766e;
}

.user-pill span,
.user-pill small {
  display: block;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card,
.panel {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
}

.stat-card {
  padding: 20px 22px;
}

.stat-card span {
  display: block;
  color: #64748b;
}

.stat-card strong {
  display: block;
  margin-top: 12px;
  font-size: 28px;
}

.tone-primary {
  border-top: 4px solid #2563eb;
}

.tone-success {
  border-top: 4px solid #16a34a;
}

.tone-warning {
  border-top: 4px solid #f59e0b;
}

.tone-danger {
  border-top: 4px solid #dc2626;
}

.panel-grid {
  display: grid;
  grid-template-columns: 1fr 1.1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.panel {
  padding: 22px 24px;
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 18px;
}

.panel-head h2 {
  margin: 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
}

.info-item {
  padding: 16px;
  border-radius: 18px;
  background: #f8fafc;
}

.info-item span {
  display: block;
  color: #64748b;
  margin-bottom: 8px;
}

.engine-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 14px;
}

.engine-card {
  padding: 16px;
  border-radius: 18px;
  background: #0f172a;
  color: #e2e8f0;
}

.engine-card h3 {
  margin: 0 0 12px;
}

.engine-card pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 12px;
  line-height: 1.5;
}

@media (max-width: 960px) {
  .topbar,
  .panel-grid {
    grid-template-columns: 1fr;
    flex-direction: column;
  }
}
</style>
