<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import {
  exportStatisticsReport,
  fetchStatisticsReport,
} from "../api/statistics";
import TeacherHeader from "../components/TeacherHeader.vue";
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();
const user = ref(null);
const loading = ref(false);
const exporting = ref(false);
<<<<<<< HEAD
=======
const exportingFrequencyChart = ref(false);
>>>>>>> 98bf8e49 (update)
const report = ref({
  dashboard: {},
  activity_frequency: [],
  activity_accuracy: [],
  activity_type_distribution: [],
});

const ACTIVITY_TYPE_LABELS = {
  class_activity: "班级活动",
  lecture: "讲座活动",
  competition: "竞赛活动",
  team_building: "团建活动",
};

const maxFrequency = computed(() => {
  const counts = report.value.activity_frequency.map((item) => item.activity_count);
  return counts.length ? Math.max(...counts) : 1;
});

const maxAccuracy = computed(() => {
  const values = report.value.activity_accuracy
    .map((item) => Number(item.accuracy || 0))
    .filter((item) => item > 0);
  return values.length ? Math.max(...values) : 1;
});

function formatActivityType(value) {
  return ACTIVITY_TYPE_LABELS[value] || value || "-";
}

async function loadReport() {
  loading.value = true;
  try {
    const response = await fetchStatisticsReport();
    report.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "统计报表加载失败");
  } finally {
    loading.value = false;
  }
}

async function downloadReport() {
  exporting.value = true;
  try {
    const response = await exportStatisticsReport();
    const blob = new Blob([response.data], {
      type: response.headers["content-type"],
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    const disposition = response.headers["content-disposition"] || "";
    const match = disposition.match(/filename=\"?([^\"]+)\"?/);
    link.href = url;
    link.download = match?.[1] || "statistics_report.xlsx";
    link.click();
    window.URL.revokeObjectURL(url);
    ElMessage.success("统计报表导出成功");
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "统计报表导出失败");
  } finally {
    exporting.value = false;
  }
}

<<<<<<< HEAD
=======
function escapeSvgText(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

async function downloadFrequencyChart() {
  if (!report.value.activity_frequency.length) {
    ElMessage.warning("暂无可导出的活动参与柱状图数据");
    return;
  }

  exportingFrequencyChart.value = true;
  try {
    const chartData = report.value.activity_frequency.slice(0, 20);
    const width = 1400;
    const rowHeight = 58;
    const topPadding = 110;
    const bottomPadding = 50;
    const height = topPadding + chartData.length * rowHeight + bottomPadding;
    const barStartX = 520;
    const barMaxWidth = 700;
    const maxCount = Math.max(...chartData.map((item) => Number(item.activity_count || 0)), 1);

    const rows = chartData
      .map((item, index) => {
        const y = topPadding + index * rowHeight;
        const count = Number(item.activity_count || 0);
        const widthValue = Math.max((count / maxCount) * barMaxWidth, 10);
        const label = `${item.student_name || "-"} (${item.student_no || "-"})`;
        const subLabel = item.class_name || "未填写班级";
        return `
          <text x="64" y="${y + 20}" font-size="18" font-weight="700" fill="#1f2937">${escapeSvgText(label)}</text>
          <text x="64" y="${y + 42}" font-size="13" fill="#6b7280">${escapeSvgText(subLabel)}</text>
          <rect x="${barStartX}" y="${y + 10}" rx="14" ry="14" width="${barMaxWidth}" height="24" fill="#e7dcc7" />
          <rect x="${barStartX}" y="${y + 10}" rx="14" ry="14" width="${widthValue}" height="24" fill="url(#barGradient)" />
          <text x="${barStartX + barMaxWidth + 28}" y="${y + 29}" font-size="20" font-weight="700" fill="#9a3412">${count}</text>
        `;
      })
      .join("");

    const svg = `
      <svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
        <defs>
          <linearGradient id="barGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#ea580c" />
            <stop offset="100%" stop-color="#f59e0b" />
          </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="#fffaf4" />
        <text x="64" y="56" font-size="32" font-weight="800" fill="#111827">学生活动参与频次柱状图</text>
        <text x="64" y="86" font-size="16" fill="#6b7280">按学生去重统计参与活动次数，展示前 20 名</text>
        ${rows}
      </svg>
    `;

    const svgBlob = new Blob([svg], { type: "image/svg+xml;charset=utf-8" });
    const svgUrl = URL.createObjectURL(svgBlob);
    const image = new Image();

    await new Promise((resolve, reject) => {
      image.onload = resolve;
      image.onerror = reject;
      image.src = svgUrl;
    });

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    const context = canvas.getContext("2d");
    if (!context) {
      throw new Error("浏览器不支持图表导出");
    }
    context.drawImage(image, 0, 0);
    URL.revokeObjectURL(svgUrl);

    const pngUrl = canvas.toDataURL("image/png");
    const link = document.createElement("a");
    link.href = pngUrl;
    link.download = `activity_frequency_chart_${new Date().toISOString().slice(0, 10)}.png`;
    link.click();
    ElMessage.success("活动参与柱状图导出成功");
  } catch (error) {
    ElMessage.error(error?.message || "活动参与柱状图导出失败");
  } finally {
    exportingFrequencyChart.value = false;
  }
}

>>>>>>> 98bf8e49 (update)
function frequencyWidth(count) {
  return `${Math.max((count / maxFrequency.value) * 100, 6)}%`;
}

function accuracyWidth(value) {
  return `${Math.max((Number(value || 0) / maxAccuracy.value) * 100, 6)}%`;
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

async function logout() {
  await performLogout(router);
}

onMounted(async () => {
  user.value = parseSavedUser();
  await loadReport();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="统计报表" current="report" :user="user" @logout="logout">
      <template #actions>
        <div class="record-actions">
          <el-button @click="loadReport">刷新数据</el-button>
          <el-button type="success" :loading="exporting" @click="downloadReport">
            导出 Excel
          </el-button>
        </div>
      </template>
    </TeacherHeader>

    <section class="stats-grid" v-loading="loading">
      <article class="stat-card">
        <span>活动总数</span>
        <strong>{{ report.dashboard.total_activities || 0 }}</strong>
      </article>
      <article class="stat-card success">
        <span>检测到的人脸总数</span>
        <strong>{{ report.dashboard.total_faces_detected || 0 }}</strong>
      </article>
      <article class="stat-card success">
        <span>累计唯一参与人数</span>
        <strong>{{ report.dashboard.total_unique_participants || 0 }}</strong>
      </article>
      <article class="stat-card warning">
        <span>平均识别准确率</span>
        <strong>{{ report.dashboard.average_accuracy || 0 }}</strong>
      </article>
    </section>

    <div class="capture-grid">
      <section class="panel">
        <div class="panel-head">
          <h2>学生活动参与频次</h2>
<<<<<<< HEAD
=======
          <el-button type="success" plain :loading="exportingFrequencyChart" @click="downloadFrequencyChart">
            导出柱状图
          </el-button>
>>>>>>> 98bf8e49 (update)
        </div>

        <div class="bar-list">
          <div
            v-for="item in report.activity_frequency"
            :key="item.student_id"
            class="bar-row"
          >
            <div class="bar-label">
              <strong>{{ item.student_name }}</strong>
              <span>{{ item.student_no }} / {{ item.class_name }}</span>
            </div>
            <div class="bar-track">
              <div class="bar-fill" :style="{ width: frequencyWidth(item.activity_count) }"></div>
            </div>
            <div class="bar-value">{{ item.activity_count }}</div>
          </div>
        </div>

        <el-table :data="report.activity_frequency" border stripe>
          <el-table-column prop="student_no" label="学号" width="120" />
          <el-table-column prop="student_name" label="姓名" width="110" />
          <el-table-column prop="class_name" label="班级" width="120" />
          <el-table-column prop="activity_count" label="参与次数" width="100" />
        </el-table>
      </section>

      <section class="panel">
        <div class="panel-head">
          <h2>活动识别准确率</h2>
        </div>

        <div class="bar-list">
          <div
            v-for="item in report.activity_accuracy"
            :key="item.activity_id"
            class="bar-row"
          >
            <div class="bar-label">
              <strong>{{ item.title }}</strong>
              <span>{{ item.activity_date }} / {{ formatActivityType(item.activity_type) }}</span>
            </div>
            <div class="bar-track">
              <div
                class="bar-fill secondary"
                :style="{ width: accuracyWidth(item.accuracy || 0) }"
              ></div>
            </div>
            <div class="bar-value">{{ item.accuracy ?? "-" }}</div>
          </div>
        </div>

        <el-table :data="report.activity_accuracy" border stripe>
          <el-table-column prop="title" label="活动名称" min-width="160" />
          <el-table-column label="活动类型" width="120">
            <template #default="{ row }">
              <span>{{ formatActivityType(row.activity_type) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="activity_date" label="日期" width="120" />
          <el-table-column prop="participant_count" label="识别参与人数" width="110" />
          <el-table-column prop="actual_student_count" label="实际参与人数" width="110" />
          <el-table-column prop="correct_match_count" label="正确识别人数" width="110" />
          <el-table-column prop="accuracy" label="准确率" width="100" />
        </el-table>
      </section>
    </div>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>活动类型分布</h2>
      </div>
      <div class="chip-grid">
        <article
          v-for="item in report.activity_type_distribution"
          :key="item.activity_type"
          class="chip-card"
        >
          <span>{{ formatActivityType(item.activity_type) }}</span>
          <strong>{{ item.count }}</strong>
        </article>
      </div>
    </section>
  </div>
</template>
