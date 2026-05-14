<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import TeacherHeader from "../components/TeacherHeader.vue";
import { fetchEmotionRecords, fetchEmotionReport } from "../api/emotions";
<<<<<<< HEAD
=======
import {
  DEFAULT_EMOTION_ORDER,
  EMOTION_OPTIONS,
  formatEmotion,
} from "../constants/emotions";
>>>>>>> 98bf8e49 (update)
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();
const user = ref(null);
const loading = ref(false);
const loadingRecords = ref(false);
const report = ref({
  dashboard: {},
  emotion_distribution: [],
  source_distribution: [],
  student_summary: [],
  daily_trend: [],
<<<<<<< HEAD
=======
  available_emotions: [],
  emotion_labels: {},
>>>>>>> 98bf8e49 (update)
});
const records = ref([]);

const filters = reactive({
  keyword: "",
  source: "",
  emotion: "",
  start_date: "",
  end_date: "",
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
const SOURCE_LABELS = {
  attendance: "考勤",
  group_photo: "合照",
};

const maxEmotionCount = computed(() => {
  const counts = report.value.emotion_distribution.map((item) => item.count);
  return counts.length ? Math.max(...counts) : 1;
});

<<<<<<< HEAD
function formatEmotion(value) {
  return EMOTION_LABELS[value] || value || "-";
}
=======
const trendEmotionKeys = computed(() => {
  const keys = report.value.available_emotions?.length
    ? report.value.available_emotions
    : report.value.emotion_distribution.map((item) => item.emotion);
  const unique = Array.from(new Set(keys.filter(Boolean)));
  const ordered = DEFAULT_EMOTION_ORDER.filter((item) => unique.includes(item));
  const extras = unique.filter((item) => !ordered.includes(item));
  return [...ordered, ...extras];
});
>>>>>>> 98bf8e49 (update)

function formatSource(value) {
  return SOURCE_LABELS[value] || value || "-";
}

function distributionWidth(count) {
  return `${Math.max((count / maxEmotionCount.value) * 100, 6)}%`;
}

function buildQuery() {
  return {
    keyword: filters.keyword || undefined,
    source: filters.source || undefined,
    emotion: filters.emotion || undefined,
    start_date: filters.start_date || undefined,
    end_date: filters.end_date || undefined,
  };
}

async function loadReport() {
  loading.value = true;
  try {
    const response = await fetchEmotionReport();
    report.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "情绪统计加载失败");
  } finally {
    loading.value = false;
  }
}

async function loadRecords() {
  loadingRecords.value = true;
  try {
    const response = await fetchEmotionRecords(buildQuery());
    records.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "情绪记录加载失败");
  } finally {
    loadingRecords.value = false;
  }
}

async function refreshAll() {
  await Promise.all([loadReport(), loadRecords()]);
}

function resetFilters() {
  filters.keyword = "";
  filters.source = "";
  filters.emotion = "";
  filters.start_date = "";
  filters.end_date = "";
  loadRecords();
}

<<<<<<< HEAD
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

function goToSystemStatus() {
  router.push({ name: "system-status" });
}

=======
>>>>>>> 98bf8e49 (update)
async function logout() {
  await performLogout(router);
}

onMounted(async () => {
  user.value = parseSavedUser();
  await refreshAll();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="情绪统计" current="emotions" :user="user" @logout="logout" />

    <section class="stats-grid" v-loading="loading">
      <article class="stat-card">
        <span>情绪记录总数</span>
        <strong>{{ report.dashboard.total_records || 0 }}</strong>
      </article>
      <article class="stat-card success">
        <span>考勤来源记录</span>
        <strong>{{ report.dashboard.attendance_records || 0 }}</strong>
      </article>
      <article class="stat-card success">
        <span>合照来源记录</span>
        <strong>{{ report.dashboard.group_photo_records || 0 }}</strong>
      </article>
      <article class="stat-card warning">
        <span>平均情绪分数</span>
        <strong>{{ report.dashboard.average_score || 0 }}</strong>
      </article>
    </section>

    <div class="capture-grid">
      <section class="panel">
        <div class="panel-head">
          <h2>情绪分布</h2>
          <el-button @click="refreshAll">刷新数据</el-button>
        </div>
        <div class="bar-list">
          <div
            v-for="item in report.emotion_distribution"
            :key="item.emotion"
            class="bar-row"
          >
            <div class="bar-label">
              <strong>{{ formatEmotion(item.emotion) }}</strong>
              <span>{{ item.emotion }}</span>
            </div>
            <div class="bar-track">
              <div
                class="bar-fill secondary"
                :style="{ width: distributionWidth(item.count) }"
              ></div>
            </div>
            <div class="bar-value">{{ item.count }}</div>
          </div>
        </div>

        <el-table :data="report.emotion_distribution" border stripe>
<<<<<<< HEAD
          <el-table-column label="情绪类型" min-width="120">
=======
          <el-table-column label="情绪类型" min-width="140">
>>>>>>> 98bf8e49 (update)
            <template #default="{ row }">
              <span>{{ formatEmotion(row.emotion) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="count" label="记录数" width="120" />
        </el-table>
      </section>

      <section class="panel">
        <div class="panel-head">
          <h2>来源分布</h2>
        </div>
        <div class="chip-grid">
          <article
            v-for="item in report.source_distribution"
            :key="item.source"
            class="chip-card"
          >
            <span>{{ formatSource(item.source) }}</span>
            <strong>{{ item.count }}</strong>
          </article>
        </div>

        <div class="panel-tip">
          当前主导情绪：
          <strong>{{ formatEmotion(report.dashboard.dominant_emotion) }}</strong>
        </div>
      </section>
    </div>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>学生情绪汇总</h2>
      </div>
      <el-table :data="report.student_summary" border stripe>
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="姓名" width="110" />
        <el-table-column prop="class_name" label="班级" width="120" />
        <el-table-column prop="record_count" label="记录数" width="90" />
<<<<<<< HEAD
        <el-table-column label="主导情绪" width="100">
=======
        <el-table-column label="主导情绪" width="110">
>>>>>>> 98bf8e49 (update)
          <template #default="{ row }">
            <span>{{ formatEmotion(row.dominant_emotion) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="average_score" label="平均分数" width="110" />
      </el-table>
    </section>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>每日趋势</h2>
      </div>
      <el-table :data="report.daily_trend" border stripe>
        <el-table-column prop="date" label="日期" width="120" />
<<<<<<< HEAD
        <el-table-column prop="happy" label="愉快" width="80" />
        <el-table-column prop="neutral" label="平静" width="80" />
        <el-table-column prop="serious" label="严肃" width="80" />
        <el-table-column prop="tired" label="疲惫" width="80" />
        <el-table-column prop="excited" label="兴奋" width="80" />
        <el-table-column prop="total" label="总数" width="80" />
=======
        <el-table-column
          v-for="emotion in trendEmotionKeys"
          :key="emotion"
          :prop="emotion"
          :label="formatEmotion(emotion)"
          width="90"
        />
        <el-table-column prop="total" label="总数" width="90" />
>>>>>>> 98bf8e49 (update)
      </el-table>
    </section>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>情绪记录</h2>
        <div class="record-actions">
          <el-button @click="resetFilters">重置筛选</el-button>
          <el-button type="primary" @click="loadRecords">查询</el-button>
        </div>
      </div>

      <el-form class="filters-form" label-position="top">
        <div class="filters-grid">
          <el-form-item label="姓名/学号/活动">
            <el-input v-model="filters.keyword" placeholder="支持学生或活动名称搜索" />
          </el-form-item>
          <el-form-item label="来源">
            <el-select v-model="filters.source" clearable placeholder="全部">
              <el-option label="考勤" value="attendance" />
              <el-option label="合照" value="group_photo" />
            </el-select>
          </el-form-item>
          <el-form-item label="情绪">
            <el-select v-model="filters.emotion" clearable placeholder="全部">
<<<<<<< HEAD
              <el-option label="愉快" value="happy" />
              <el-option label="平静" value="neutral" />
              <el-option label="严肃" value="serious" />
              <el-option label="疲惫" value="tired" />
              <el-option label="兴奋" value="excited" />
=======
              <el-option
                v-for="item in EMOTION_OPTIONS"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
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
        <el-table-column label="来源" width="90">
          <template #default="{ row }">
            <span>{{ formatSource(row.source) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="student_no" label="学号" width="120" />
        <el-table-column prop="student_name" label="姓名" width="110" />
        <el-table-column prop="class_name" label="班级" width="120" />
        <el-table-column prop="activity_title" label="活动名称" min-width="160" />
<<<<<<< HEAD
        <el-table-column label="情绪" width="100">
=======
        <el-table-column label="情绪" width="110">
>>>>>>> 98bf8e49 (update)
          <template #default="{ row }">
            <span>{{ formatEmotion(row.emotion) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="emotion_score" label="分数" width="100" />
<<<<<<< HEAD
        <el-table-column prop="emotion_mode" label="模式" width="180" />
=======
        <el-table-column prop="emotion_mode" label="模式" width="220" />
>>>>>>> 98bf8e49 (update)
        <el-table-column prop="created_at" label="识别时间" min-width="180" />
      </el-table>
    </section>
  </div>
</template>
