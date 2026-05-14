<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import TeacherHeader from "../components/TeacherHeader.vue";
<<<<<<< HEAD
import { fetchAuditLogRecords, fetchAuditLogSummary } from "../api/auditLogs";
=======
import {
  exportAuditLogRecords,
  fetchAuditLogRecords,
  fetchAuditLogSummary,
} from "../api/auditLogs";
>>>>>>> 98bf8e49 (update)
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();

const user = ref(null);
const loading = ref(false);
<<<<<<< HEAD
=======
const exporting = ref(false);
>>>>>>> 98bf8e49 (update)
const records = ref([]);
const summary = ref({
  total_count: 0,
  today_count: 0,
  success_count: 0,
  failed_count: 0,
  unique_operator_count: 0,
  module_distribution: [],
  action_distribution: [],
});

const filters = reactive({
  keyword: "",
  module: "",
  action: "",
  result: "",
  operator_username: "",
<<<<<<< HEAD
=======
  target_name: "",
>>>>>>> 98bf8e49 (update)
  start_date: "",
  end_date: "",
});

const detailDialogVisible = ref(false);
const selectedLog = ref(null);

const moduleOptions = [
  { label: "认证", value: "auth" },
  { label: "用户管理", value: "user_management" },
  { label: "学生管理", value: "student_management" },
  { label: "考勤", value: "attendance" },
  { label: "安全测试", value: "security_test" },
  { label: "合照识别", value: "group_photo" },
  { label: "统计报表", value: "statistics" },
];

const actionOptions = [
  { label: "登录", value: "login" },
  { label: "退出登录", value: "logout" },
  { label: "修改密码", value: "change_password" },
  { label: "创建用户", value: "create_user" },
  { label: "更新用户", value: "update_user" },
  { label: "重置密码", value: "reset_password" },
  { label: "删除用户", value: "delete_user" },
  { label: "创建学生", value: "create_student" },
  { label: "更新学生", value: "update_student" },
  { label: "导入学生", value: "import_students" },
  { label: "上传注册照", value: "upload_student_face" },
  { label: "绑定学生账号", value: "bind_student_account" },
  { label: "重置学生密码", value: "reset_student_password" },
  { label: "删除学生", value: "delete_student" },
  { label: "考勤识别", value: "checkin" },
  { label: "导出考勤", value: "export_attendance" },
  { label: "活体安全测试", value: "run_liveness_test" },
  { label: "合照识别", value: "recognize_group_photo" },
  { label: "活动评估", value: "evaluate_activity" },
  { label: "导出统计报表", value: "export_statistics_report" },
];

const topModules = computed(() => summary.value.module_distribution.slice(0, 8));
const topActions = computed(() => summary.value.action_distribution.slice(0, 8));

const detailText = computed(() =>
  selectedLog.value?.detail ? JSON.stringify(selectedLog.value.detail, null, 2) : "{}"
);

function buildQuery() {
  return {
    keyword: filters.keyword || undefined,
    module: filters.module || undefined,
    action: filters.action || undefined,
    result: filters.result || undefined,
    operator_username: filters.operator_username || undefined,
<<<<<<< HEAD
=======
    target_name: filters.target_name || undefined,
>>>>>>> 98bf8e49 (update)
    start_date: filters.start_date || undefined,
    end_date: filters.end_date || undefined,
  };
}

function formatModule(value) {
  return (
    moduleOptions.find((item) => item.value === value)?.label ||
    value ||
    "-"
  );
}

function formatAction(value) {
  return (
    actionOptions.find((item) => item.value === value)?.label ||
    value ||
    "-"
  );
}

function formatRole(value) {
  return value === "teacher" ? "教师" : value === "student" ? "学生" : value || "-";
}

function resultTagType(value) {
  return value === "success" ? "success" : "danger";
}

function resultLabel(value) {
  return value === "success" ? "成功" : value === "failed" ? "失败" : value || "-";
}

async function loadLogs() {
  loading.value = true;
  try {
    const [recordsResponse, summaryResponse] = await Promise.all([
      fetchAuditLogRecords(buildQuery()),
      fetchAuditLogSummary(buildQuery()),
    ]);
    records.value = recordsResponse.data;
    summary.value = summaryResponse.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "审计日志加载失败");
  } finally {
    loading.value = false;
  }
}

<<<<<<< HEAD
=======
async function downloadLogs() {
  exporting.value = true;
  try {
    const response = await exportAuditLogRecords(buildQuery());
    const blob = new Blob([response.data], {
      type: response.headers["content-type"],
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    const disposition = response.headers["content-disposition"] || "";
    const match = disposition.match(/filename="?([^"]+)"?/);
    link.href = url;
    link.download = match?.[1] || "audit_logs.xlsx";
    link.click();
    window.URL.revokeObjectURL(url);
    ElMessage.success("操作日志导出成功");
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "操作日志导出失败");
  } finally {
    exporting.value = false;
  }
}

>>>>>>> 98bf8e49 (update)
function resetFilters() {
  filters.keyword = "";
  filters.module = "";
  filters.action = "";
  filters.result = "";
  filters.operator_username = "";
<<<<<<< HEAD
=======
  filters.target_name = "";
>>>>>>> 98bf8e49 (update)
  filters.start_date = "";
  filters.end_date = "";
  loadLogs();
}

function openDetail(row) {
  selectedLog.value = row;
  detailDialogVisible.value = true;
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

function goToTeacherProfile() {
  router.push({ name: "teacher-profile" });
}

function goToSystemStatus() {
  router.push({ name: "system-status" });
}

async function logout() {
  await performLogout(router);
}

onMounted(async () => {
  user.value = parseSavedUser();
  await loadLogs();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="操作日志" current="audit-logs" :user="user" @logout="logout" />

    <section class="stats-grid" v-loading="loading">
      <article class="stat-card">
        <span>日志总数</span>
        <strong>{{ summary.total_count || 0 }}</strong>
      </article>
      <article class="stat-card success">
        <span>今日记录</span>
        <strong>{{ summary.today_count || 0 }}</strong>
      </article>
      <article class="stat-card danger">
        <span>失败操作</span>
        <strong>{{ summary.failed_count || 0 }}</strong>
      </article>
      <article class="stat-card warning">
        <span>操作人数量</span>
        <strong>{{ summary.unique_operator_count || 0 }}</strong>
      </article>
    </section>

    <div class="capture-grid admin-grid">
      <section class="panel">
        <div class="panel-head">
          <h2>模块分布</h2>
        </div>
        <div class="chip-grid">
          <article v-for="item in topModules" :key="item.module" class="chip-card">
            <span>{{ formatModule(item.module) }}</span>
            <strong>{{ item.count }}</strong>
          </article>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <h2>动作分布</h2>
        </div>
        <div class="chip-grid">
          <article v-for="item in topActions" :key="item.action" class="chip-card">
            <span>{{ formatAction(item.action) }}</span>
            <strong>{{ item.count }}</strong>
          </article>
        </div>
      </section>
    </div>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>审计日志检索</h2>
        <div class="record-actions">
          <el-button @click="resetFilters">重置筛选</el-button>
          <el-button type="primary" @click="loadLogs">查询</el-button>
<<<<<<< HEAD
=======
          <el-button type="success" :loading="exporting" @click="downloadLogs">导出 Excel</el-button>
>>>>>>> 98bf8e49 (update)
        </div>
      </div>

      <el-form class="filters-form" label-position="top">
        <div class="filters-grid">
          <el-form-item label="关键词">
            <el-input
              v-model="filters.keyword"
              placeholder="按模块、动作、消息、目标对象搜索"
            />
          </el-form-item>
          <el-form-item label="模块">
            <el-select v-model="filters.module" clearable placeholder="全部">
              <el-option
                v-for="item in moduleOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="动作">
            <el-select v-model="filters.action" clearable placeholder="全部">
              <el-option
                v-for="item in actionOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="结果">
            <el-select v-model="filters.result" clearable placeholder="全部">
              <el-option label="成功" value="success" />
              <el-option label="失败" value="failed" />
            </el-select>
          </el-form-item>
          <el-form-item label="操作用户名">
            <el-input v-model="filters.operator_username" placeholder="如：teacher" />
          </el-form-item>
<<<<<<< HEAD
=======
          <el-form-item label="目标对象">
            <el-input v-model="filters.target_name" placeholder="按目标对象名称筛选" />
          </el-form-item>
>>>>>>> 98bf8e49 (update)
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

      <el-table :data="records" v-loading="loading" border stripe>
        <el-table-column prop="created_at" label="时间" min-width="170" />
        <el-table-column prop="operator_username" label="操作人" width="120" />
        <el-table-column label="角色" width="90">
          <template #default="{ row }">
            <span>{{ formatRole(row.operator_role) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="模块" width="110">
          <template #default="{ row }">
            <span>{{ formatModule(row.module) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="动作" width="140">
          <template #default="{ row }">
            <span>{{ formatAction(row.action) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="target_name" label="目标对象" min-width="150" />
        <el-table-column label="结果" width="90">
          <template #default="{ row }">
            <el-tag :type="resultTagType(row.result)">
              {{ resultLabel(row.result) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="消息" min-width="220" show-overflow-tooltip />
        <el-table-column label="详情" width="100" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openDetail(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <el-dialog
      v-model="detailDialogVisible"
      title="日志详情"
      width="700px"
      destroy-on-close
    >
      <div v-if="selectedLog" class="result-card">
        <div class="result-grid">
          <div>
            <span>时间</span>
            <strong>{{ selectedLog.created_at }}</strong>
          </div>
          <div>
            <span>操作人</span>
            <strong>{{ selectedLog.operator_username || "-" }}</strong>
          </div>
          <div>
            <span>模块</span>
            <strong>{{ formatModule(selectedLog.module) }}</strong>
          </div>
          <div>
            <span>动作</span>
            <strong>{{ formatAction(selectedLog.action) }}</strong>
          </div>
          <div>
            <span>结果</span>
            <strong>{{ resultLabel(selectedLog.result) }}</strong>
          </div>
          <div>
            <span>目标对象</span>
            <strong>{{ selectedLog.target_name || "-" }}</strong>
          </div>
        </div>
      </div>
      <pre class="detail-box">{{ detailText }}</pre>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.admin-grid {
  grid-template-columns: 1fr 1fr;
}

.detail-box {
  margin: 16px 0 0;
  padding: 16px;
  border-radius: 20px;
  background: rgba(255, 250, 244, 0.72);
  border: 1px solid var(--line);
  color: var(--text);
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 320px;
  overflow: auto;
}
</style>
