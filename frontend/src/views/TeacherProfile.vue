<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import { changePassword, fetchCurrentUser } from "../api/auth";
import TeacherHeader from "../components/TeacherHeader.vue";
import { fetchSystemSummary } from "../api/system";
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();

const user = ref(null);
const profile = ref(null);
const systemSummary = ref({
  user_count: 0,
  student_count: 0,
  attendance_count: 0,
});
const loading = ref(false);
const passwordSubmitting = ref(false);

const passwordForm = reactive({
  current_password: "",
  new_password: "",
  confirm_password: "",
});

const summaryCards = computed(() => [
  {
    key: "users",
    label: "系统用户数",
    value: systemSummary.value.user_count || 0,
    tone: "primary",
  },
  {
    key: "students",
    label: "学生档案数",
    value: systemSummary.value.student_count || 0,
    tone: "success",
  },
  {
    key: "attendance",
    label: "考勤记录数",
    value: systemSummary.value.attendance_count || 0,
    tone: "warning",
  },
]);

function resetPasswordForm() {
  passwordForm.current_password = "";
  passwordForm.new_password = "";
  passwordForm.confirm_password = "";
}

async function loadProfile() {
  loading.value = true;
  try {
    const [profileResponse, summaryResponse] = await Promise.all([
      fetchCurrentUser(),
      fetchSystemSummary(),
    ]);
    profile.value = profileResponse.data;
    systemSummary.value = summaryResponse.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "教师信息加载失败");
  } finally {
    loading.value = false;
  }
}

async function submitPasswordChange() {
  if (!passwordForm.current_password || !passwordForm.new_password) {
    ElMessage.warning("请完整填写当前密码和新密码");
    return;
  }
  if (passwordForm.new_password.length < 6) {
    ElMessage.warning("新密码长度不能少于 6 位");
    return;
  }
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    ElMessage.warning("两次输入的新密码不一致");
    return;
  }

  passwordSubmitting.value = true;
  try {
    await changePassword({
      current_password: passwordForm.current_password,
      new_password: passwordForm.new_password,
    });
    ElMessage.success("密码修改成功");
    resetPasswordForm();
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "密码修改失败");
  } finally {
    passwordSubmitting.value = false;
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

function goToSystemStatus() {
  router.push({ name: "system-status" });
}

onMounted(async () => {
  user.value = parseSavedUser();
  await loadProfile();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="教师中心" current="teacher-profile" :user="user" @logout="logout" />

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

    <div class="overview-grid">
      <section class="panel" v-loading="loading">
        <div class="panel-head">
          <h2>账号信息</h2>
          <el-button @click="loadProfile">刷新</el-button>
        </div>
        <div v-if="profile" class="info-grid">
          <article class="info-item">
            <span>用户 ID</span>
            <strong>{{ profile.id }}</strong>
          </article>
          <article class="info-item">
            <span>用户名</span>
            <strong>{{ profile.username }}</strong>
          </article>
          <article class="info-item">
            <span>角色</span>
            <strong>{{ profile.role }}</strong>
          </article>
          <article class="info-item">
            <span>账号状态</span>
            <el-tag :type="profile.is_active ? 'success' : 'danger'">
              {{ profile.is_active ? "启用" : "停用" }}
            </el-tag>
          </article>
          <article class="info-item">
            <span>创建时间</span>
            <strong>{{ profile.created_at || "-" }}</strong>
          </article>
          <article class="info-item">
            <span>绑定学生</span>
            <strong>{{ profile.student_id || "-" }}</strong>
          </article>
        </div>
        <el-empty v-else description="暂无教师账户信息" />
      </section>

      <section class="panel">
        <div class="panel-head">
          <h2>密码维护</h2>
        </div>
        <el-form label-position="top" class="password-form">
          <el-form-item label="当前密码">
            <el-input
              v-model="passwordForm.current_password"
              type="password"
              show-password
              placeholder="请输入当前密码"
            />
          </el-form-item>
          <el-form-item label="新密码">
            <el-input
              v-model="passwordForm.new_password"
              type="password"
              show-password
              placeholder="请输入新密码"
            />
          </el-form-item>
          <el-form-item label="确认新密码">
            <el-input
              v-model="passwordForm.confirm_password"
              type="password"
              show-password
              placeholder="请再次输入新密码"
              @keyup.enter="submitPasswordChange"
            />
          </el-form-item>
          <div class="form-actions">
            <el-button @click="resetPasswordForm">重置</el-button>
            <el-button type="primary" :loading="passwordSubmitting" @click="submitPasswordChange">
              修改密码
            </el-button>
          </div>
        </el-form>
      </section>
    </div>

    <section class="panel quick-actions">
      <div class="panel-head">
        <h2>快捷入口</h2>
      </div>
      <div class="action-grid">
        <button class="action-card" @click="goToAttendance">
          <strong>前往考勤页</strong>
          <span>继续进行摄像头考勤与记录导出</span>
        </button>
        <button class="action-card" @click="goToStudents">
          <strong>前往学生管理</strong>
          <span>录入学生、绑定账号、上传注册照</span>
        </button>
        <button class="action-card" @click="goToUsers">
          <strong>前往用户管理</strong>
          <span>维护教师账号并查看权限矩阵</span>
        </button>
        <button class="action-card" @click="goToSystemStatus">
          <strong>查看系统状态</strong>
          <span>确认模型加载、设备和系统摘要</span>
        </button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page-shell {
  min-height: 100vh;
  padding: 24px;
  background:
    radial-gradient(circle at top left, rgba(37, 99, 235, 0.12), transparent 28%),
    radial-gradient(circle at top right, rgba(249, 115, 22, 0.14), transparent 22%),
    #f5f7fb;
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
  color: #2563eb;
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
  background: #eff6ff;
  color: #1d4ed8;
}

.user-pill span,
.user-pill small {
  display: block;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.stat-card,
.panel {
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.94);
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
  font-size: 30px;
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

.overview-grid {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
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

.password-form {
  max-width: 560px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.action-card {
  border: 0;
  padding: 18px;
  text-align: left;
  border-radius: 20px;
  background: linear-gradient(135deg, #eff6ff, #fff7ed);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 30px rgba(15, 23, 42, 0.1);
}

.action-card strong,
.action-card span {
  display: block;
}

.action-card span {
  margin-top: 10px;
  color: #475569;
}

@media (max-width: 960px) {
  .topbar,
  .overview-grid {
    grid-template-columns: 1fr;
    flex-direction: column;
  }
}
</style>
