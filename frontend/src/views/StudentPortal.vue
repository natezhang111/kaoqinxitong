<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import { fetchAttendanceRecords } from "../api/attendance";
import { changePassword } from "../api/auth";
import {
  fetchMyStudentActivities,
  fetchMyStudentEmotions,
  fetchMyStudentGroupPhotoRecords,
  fetchMyStudentProfile,
} from "../api/students";
<<<<<<< HEAD
=======
import { formatEmotion as formatEmotionLabel } from "../constants/emotions";
>>>>>>> 98bf8e49 (update)

const router = useRouter();

const user = ref(null);
const loading = ref(false);
const passwordSubmitting = ref(false);
const activeTab = ref("attendance");

const profile = ref(null);
const activities = ref([]);
const emotions = ref([]);
const attendanceRecords = ref([]);
const groupPhotoRecords = ref([]);

const passwordDialogVisible = ref(false);
const passwordForm = reactive({
  current_password: "",
  new_password: "",
  confirm_password: "",
});

<<<<<<< HEAD
const EMOTION_LABELS = {
  happy: "愉快",
  neutral: "平静",
  serious: "严肃",
  tired: "疲惫",
  excited: "兴奋",
};

=======
>>>>>>> 98bf8e49 (update)
const ACTIVITY_TYPE_LABELS = {
  class_activity: "班级活动",
  lecture: "讲座活动",
  competition: "竞赛活动",
  team_building: "团建活动",
};

const ATTENDANCE_STATUS_LABELS = {
  present: "考勤成功",
  rejected: "已拒绝",
  unknown: "未匹配",
};

const CAPTURE_MODE_LABELS = {
  manual: "手动抓拍",
  auto: "自动抓拍",
  upload: "图片上传",
};

const LIVENESS_LABELS = {
  passed: "通过",
  failed: "未通过",
  skipped: "未检测",
};

const summaryCards = computed(() => [
  {
    key: "attendance",
    label: "我的考勤",
    value: profile.value?.summary?.attendance_count || 0,
    tone: "default",
  },
  {
    key: "present",
    label: "成功次数",
    value: profile.value?.summary?.present_count || 0,
    tone: "success",
  },
  {
    key: "activity",
    label: "参与活动",
    value: profile.value?.summary?.activity_count || 0,
    tone: "primary",
  },
  {
    key: "emotion",
    label: "情绪记录",
    value: profile.value?.summary?.emotion_count || 0,
    tone: "warning",
  },
]);

const latestEmotion = computed(() => emotions.value[0] || null);

const portalAlert = computed(() => {
  if (!profile.value) {
    return {
      type: "info",
      title: "正在加载学生信息",
      description: "页面会自动拉取你的个人档案、考勤、活动和情绪记录。",
    };
  }

  if (!profile.value.account_is_active) {
    return {
      type: "error",
      title: "当前学生账号已停用",
      description: "请联系教师在学生管理页重新启用你的账号。",
    };
  }

  if (profile.value.feature_status !== "ready") {
    return {
      type: "warning",
      title: "人脸特征尚未准备完成",
      description: "当前可能无法稳定完成考勤或合照识别，请联系教师补传注册照并提取特征。",
    };
  }

  return {
    type: "success",
    title: "学生账号状态正常",
    description: "你可以直接查看个人考勤、合照参与记录和情绪记录，也可以在此修改登录密码。",
  };
});

function parseSavedUser() {
  const raw = localStorage.getItem("attendance_user");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function formatEmotion(value) {
<<<<<<< HEAD
  return EMOTION_LABELS[value] || value || "-";
=======
  return formatEmotionLabel(value);
>>>>>>> 98bf8e49 (update)
}

function formatActivityType(value) {
  return ACTIVITY_TYPE_LABELS[value] || value || "-";
}

function formatAttendanceStatus(value) {
  return ATTENDANCE_STATUS_LABELS[value] || value || "-";
}

function formatCaptureMode(value) {
  return CAPTURE_MODE_LABELS[value] || value || "-";
}

function formatLiveness(value) {
  return LIVENESS_LABELS[value] || value || "-";
}

function resetPasswordForm() {
  passwordForm.current_password = "";
  passwordForm.new_password = "";
  passwordForm.confirm_password = "";
}

async function loadPortal() {
  loading.value = true;
  try {
    const [
      profileResponse,
      activitiesResponse,
      emotionsResponse,
      attendanceResponse,
      groupPhotoResponse,
    ] = await Promise.all([
      fetchMyStudentProfile(),
      fetchMyStudentActivities(),
      fetchMyStudentEmotions(),
      fetchAttendanceRecords(),
      fetchMyStudentGroupPhotoRecords(),
    ]);

    profile.value = profileResponse.data;
    activities.value = activitiesResponse.data;
    emotions.value = emotionsResponse.data;
    attendanceRecords.value = attendanceResponse.data;
    groupPhotoRecords.value = groupPhotoResponse.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "学生端数据加载失败");
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
    ElMessage.success("密码修改成功，下次登录请使用新密码");
    passwordDialogVisible.value = false;
    resetPasswordForm();
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "密码修改失败");
  } finally {
    passwordSubmitting.value = false;
  }
}

function openPasswordDialog() {
  resetPasswordForm();
  passwordDialogVisible.value = true;
}

function logout() {
  localStorage.removeItem("attendance_token");
  localStorage.removeItem("attendance_user");
  router.push({ name: "login" });
}

onMounted(async () => {
  user.value = parseSavedUser();
  await loadPortal();
});
</script>

<template>
  <div class="page-shell">
    <header class="topbar">
      <div>
        <p class="eyebrow">Student Portal</p>
        <h1>学生个人中心</h1>
        <p class="subcopy">集中查看本人考勤、活动参与、合照记录与情绪信息。</p>
      </div>
      <div class="topbar-actions">
        <div class="user-pill">
          <span>{{ user?.username || "未登录" }}</span>
          <small>{{ user?.role || "-" }}</small>
        </div>
        <el-button @click="loadPortal">刷新数据</el-button>
        <el-button type="primary" plain @click="openPasswordDialog">修改密码</el-button>
        <el-button plain @click="logout">退出登录</el-button>
      </div>
    </header>

    <el-alert
      class="portal-alert"
      :title="portalAlert.title"
      :description="portalAlert.description"
      :type="portalAlert.type"
      show-icon
      :closable="false"
    />

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
      <section class="panel">
        <div class="panel-head">
          <h2>个人信息</h2>
        </div>
        <div v-if="profile" class="info-grid">
          <article class="info-item">
            <span>学号</span>
            <strong>{{ profile.student_no }}</strong>
          </article>
          <article class="info-item">
            <span>姓名</span>
            <strong>{{ profile.name }}</strong>
          </article>
          <article class="info-item">
            <span>班级</span>
            <strong>{{ profile.class_name }}</strong>
          </article>
          <article class="info-item">
            <span>登录账号</span>
            <strong>{{ profile.account_username || user?.username || "-" }}</strong>
          </article>
          <article class="info-item">
            <span>账号状态</span>
            <el-tag :type="profile.account_is_active ? 'success' : 'danger'">
              {{ profile.account_is_active ? "启用" : "停用" }}
            </el-tag>
          </article>
          <article class="info-item">
            <span>人脸特征状态</span>
            <el-tag :type="profile.feature_status === 'ready' ? 'success' : 'warning'">
              {{ profile.feature_status }}
            </el-tag>
          </article>
        </div>
        <el-empty v-else description="暂无学生档案数据" />
      </section>

      <section class="panel">
        <div class="panel-head">
          <h2>最近情绪</h2>
        </div>
        <div v-if="latestEmotion" class="info-grid">
          <article class="info-item">
            <span>情绪标签</span>
            <strong>{{ formatEmotion(latestEmotion.emotion) }}</strong>
          </article>
          <article class="info-item">
            <span>情绪分数</span>
            <strong>{{ latestEmotion.emotion_score ?? "-" }}</strong>
          </article>
          <article class="info-item">
            <span>来源</span>
            <strong>{{ latestEmotion.source_label || "-" }}</strong>
          </article>
          <article class="info-item">
            <span>识别时间</span>
            <strong>{{ latestEmotion.created_at || "-" }}</strong>
          </article>
        </div>
        <el-empty v-else description="当前还没有个人情绪记录" />
      </section>
    </div>

    <section class="panel main-panel">
      <div class="panel-head">
        <h2>个人记录</h2>
      </div>

      <el-tabs v-model="activeTab">
        <el-tab-pane
          :label="`我的考勤 (${attendanceRecords.length})`"
          name="attendance"
        >
          <el-table :data="attendanceRecords" border stripe>
            <el-table-column prop="created_at" label="时间" min-width="170" />
            <el-table-column label="状态" width="110">
              <template #default="{ row }">
                <el-tag
                  :type="
                    row.status === 'present'
                      ? 'success'
                      : row.status === 'rejected'
                        ? 'danger'
                        : 'warning'
                  "
                >
                  {{ formatAttendanceStatus(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="采集方式" width="120">
              <template #default="{ row }">
                <span>{{ formatCaptureMode(row.capture_mode) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="活体结果" width="110">
              <template #default="{ row }">
                <span>{{ formatLiveness(row.liveness_result) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="情绪" width="100">
              <template #default="{ row }">
                <span>{{ formatEmotion(row.emotion) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="emotion_score" label="情绪分数" width="110" />
            <el-table-column prop="match_score" label="匹配分数" width="110" />
          </el-table>
          <el-empty
            v-if="!attendanceRecords.length"
            description="当前还没有个人考勤记录"
          />
        </el-tab-pane>

        <el-tab-pane
          :label="`活动参与 (${activities.length})`"
          name="activities"
        >
          <el-table :data="activities" border stripe>
            <el-table-column prop="title" label="活动名称" min-width="180" />
            <el-table-column label="活动类型" width="120">
              <template #default="{ row }">
                <span>{{ formatActivityType(row.activity_type) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="activity_date" label="活动日期" width="120" />
            <el-table-column prop="match_score" label="最佳匹配分数" width="120" />
            <el-table-column label="情绪" width="100">
              <template #default="{ row }">
                <span>{{ formatEmotion(row.emotion) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="emotion_score" label="情绪分数" width="110" />
            <el-table-column prop="created_at" label="记录时间" min-width="170" />
          </el-table>
          <el-empty
            v-if="!activities.length"
            description="当前还没有活动参与记录"
          />
        </el-tab-pane>

        <el-tab-pane
          :label="`合照记录 (${groupPhotoRecords.length})`"
          name="group-photos"
        >
          <el-table :data="groupPhotoRecords" border stripe>
            <el-table-column prop="title" label="活动名称" min-width="180" />
            <el-table-column label="活动类型" width="120">
              <template #default="{ row }">
                <span>{{ formatActivityType(row.activity_type) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="activity_date" label="活动日期" width="120" />
            <el-table-column prop="recognized_face_count" label="识别到本人次数" width="130" />
            <el-table-column prop="participant_count" label="参与人数" width="100" />
            <el-table-column prop="best_match_score" label="最佳匹配分数" width="130" />
            <el-table-column prop="average_match_score" label="平均匹配分数" width="130" />
            <el-table-column label="最近情绪" width="110">
              <template #default="{ row }">
                <span>{{ formatEmotion(row.latest_emotion) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="latest_recognized_at" label="最近识别时间" min-width="170" />
          </el-table>
          <el-empty
            v-if="!groupPhotoRecords.length"
            description="当前还没有合照参与记录"
          />
        </el-tab-pane>

        <el-tab-pane
          :label="`情绪记录 (${emotions.length})`"
          name="emotions"
        >
          <el-table :data="emotions" border stripe>
            <el-table-column prop="created_at" label="识别时间" min-width="170" />
            <el-table-column prop="source_label" label="来源" width="120" />
            <el-table-column prop="activity_title" label="活动名称" min-width="160" />
            <el-table-column label="情绪" width="100">
              <template #default="{ row }">
                <span>{{ formatEmotion(row.emotion) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="emotion_score" label="情绪分数" width="110" />
            <el-table-column prop="emotion_mode" label="识别模式" min-width="180" />
          </el-table>
          <el-empty
            v-if="!emotions.length"
            description="当前还没有情绪记录"
          />
        </el-tab-pane>
      </el-tabs>
    </section>

    <el-dialog
      v-model="passwordDialogVisible"
      title="修改登录密码"
      width="420px"
      destroy-on-close
    >
      <el-form label-position="top">
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
            placeholder="请输入新密码，至少 6 位"
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
      </el-form>

      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="passwordSubmitting"
          @click="submitPasswordChange"
        >
          保存新密码
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.portal-alert {
  margin-bottom: 18px;
}

.subcopy {
  margin: 6px 0 0;
  color: #5f6b7a;
  font-size: 14px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.main-panel {
  margin-top: 0;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px 16px;
  border-radius: 14px;
  background: #f6f8fc;
}

.info-item span {
  font-size: 13px;
  color: #6b7280;
}

.info-item strong {
  color: #1f2937;
  font-size: 15px;
  word-break: break-all;
}

.stat-card.tone-default {
  border-left: 4px solid #3b82f6;
}

.stat-card.tone-success {
  border-left: 4px solid #10b981;
}

.stat-card.tone-primary {
  border-left: 4px solid #2563eb;
}

.stat-card.tone-warning {
  border-left: 4px solid #f59e0b;
}

@media (max-width: 960px) {
  .overview-grid {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }
}
</style>
