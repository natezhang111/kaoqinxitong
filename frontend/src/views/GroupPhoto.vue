<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import {
  correctGroupPhotoFaceResult,
  evaluateActivity,
  exportGroupPhotoActivity,
  fetchActivities,
  fetchActivityDetail,
  recognizeGroupPhoto,
} from "../api/groupPhotos";
<<<<<<< HEAD
=======
import { formatEmotion as formatEmotionLabel } from "../constants/emotions";
>>>>>>> 98bf8e49 (update)
import TeacherHeader from "../components/TeacherHeader.vue";
import { fetchStudents } from "../api/students";
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();

const user = ref(null);
const loading = ref(false);
const submitting = ref(false);
const evaluating = ref(false);
const exporting = ref(false);
const correcting = ref(false);
const selectedPhotoFile = ref(null);
const selectedPhotoPreview = ref("");
const latestResult = ref(null);

const activities = ref([]);
const students = ref([]);
const detailDialogVisible = ref(false);
const detailLoading = ref(false);
const activityDetail = ref(null);
const correctionDialogVisible = ref(false);
const selectedFaceResult = ref(null);

const filters = reactive({
  keyword: "",
  activity_type: "",
  activity_date: "",
});

const uploadForm = reactive({
  title: "",
  activityType: "class_activity",
  activityDate: "",
});

const evaluateForm = reactive({
  activityId: null,
  actual_student_count: "",
  correct_match_count: "",
  remark: "",
});

const correctionForm = reactive({
  action: "assign_student",
  student_id: null,
  note: "",
});

const ACTIVITY_TYPE_LABELS = {
  class_activity: "班级活动",
  lecture: "讲座活动",
  competition: "竞赛活动",
  team_building: "团建活动",
};

const REVIEW_ACTION_LABELS = {
  assign_student: "改派学生",
  mark_unknown: "改为未知",
};

const activityStats = computed(() => {
  const total = activities.value.length;
  const totalFaces = activities.value.reduce(
    (sum, item) => sum + Number(item.face_count || 0),
    0
  );
  const totalMatched = activities.value.reduce(
    (sum, item) => sum + Number(item.matched_count || 0),
    0
  );
  const evaluated = activities.value.filter(
    (item) => item.evaluation_accuracy !== undefined && item.evaluation_accuracy !== null
  );
  const averageAccuracy =
    evaluated.length > 0
      ? (
          evaluated.reduce(
            (sum, item) => sum + Number(item.evaluation_accuracy || 0),
            0
          ) / evaluated.length
        ).toFixed(3)
      : "0.000";

  return {
    total,
    totalFaces,
    totalMatched,
    averageAccuracy,
  };
});

const expectedAccuracy = computed(() => {
  const actual = Number(evaluateForm.actual_student_count);
  const correct = Number(evaluateForm.correct_match_count);
  if (!actual || Number.isNaN(actual) || Number.isNaN(correct) || actual <= 0) {
    return null;
  }
  return (correct / actual).toFixed(4);
});

function buildQuery() {
  return {
    keyword: filters.keyword || undefined,
    activity_type: filters.activity_type || undefined,
    activity_date: filters.activity_date || undefined,
  };
}

function formatActivityType(value) {
  return ACTIVITY_TYPE_LABELS[value] || value || "-";
}

function formatStatus(value) {
  return value === "matched" ? "已匹配" : value === "unknown" ? "未匹配" : value || "-";
}

function formatReviewAction(value) {
  return REVIEW_ACTION_LABELS[value] || value || "-";
}

<<<<<<< HEAD
=======
function formatEmotion(value) {
  return formatEmotionLabel(value);
}

function buildActivityImageUrl(imagePath) {
  if (!imagePath) {
    return "";
  }
  if (imagePath.startsWith("http://") || imagePath.startsWith("https://")) {
    return imagePath;
  }
  return imagePath.startsWith("/") ? imagePath : `/${imagePath}`;
}

>>>>>>> 98bf8e49 (update)
function statusTagType(value) {
  return value === "matched" ? "success" : "warning";
}

function reviewTagType(value) {
  return value === "reviewed" ? "primary" : "info";
}

async function loadStudents() {
  try {
    const response = await fetchStudents({ is_active: true });
    students.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "学生列表加载失败");
  }
}

async function loadActivities() {
  loading.value = true;
  try {
    const response = await fetchActivities(buildQuery());
    activities.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "活动记录加载失败");
  } finally {
    loading.value = false;
  }
}

function resetFilters() {
  filters.keyword = "";
  filters.activity_type = "";
  filters.activity_date = "";
  loadActivities();
}

function handlePhotoChange(uploadFile) {
  if (!uploadFile?.raw) {
    selectedPhotoFile.value = null;
    selectedPhotoPreview.value = "";
    return;
  }
  selectedPhotoFile.value = uploadFile.raw;
  selectedPhotoPreview.value = URL.createObjectURL(uploadFile.raw);
}

async function submitGroupPhoto() {
  if (!selectedPhotoFile.value) {
    ElMessage.warning("请先选择活动合照");
    return;
  }
  if (!uploadForm.title.trim()) {
    ElMessage.warning("请输入活动名称");
    return;
  }

  submitting.value = true;
  try {
    const response = await recognizeGroupPhoto({
      file: selectedPhotoFile.value,
      title: uploadForm.title,
      activityType: uploadForm.activityType,
      activityDate: uploadForm.activityDate,
    });
    latestResult.value = response.data;
    evaluateForm.activityId = response.data.activity_id;
    evaluateForm.actual_student_count = response.data.participant_count || "";
    evaluateForm.correct_match_count = response.data.participant_count || "";
    evaluateForm.remark = "";
    ElMessage.success("合照识别完成");
    await loadActivities();
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "合照识别失败");
  } finally {
    submitting.value = false;
  }
}

async function openActivityDetail(activity) {
  detailLoading.value = true;
  detailDialogVisible.value = true;
  try {
    const response = await fetchActivityDetail(activity.id);
    activityDetail.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "活动详情加载失败");
    detailDialogVisible.value = false;
  } finally {
    detailLoading.value = false;
  }
}

function fillEvaluationForm(activity) {
  evaluateForm.activityId = activity.id;
  evaluateForm.actual_student_count =
    activity.evaluation_actual_student_count || activity.participant_count || "";
  evaluateForm.correct_match_count =
    activity.evaluation_correct_match_count || activity.participant_count || "";
  evaluateForm.remark = "";
}

async function submitEvaluation() {
  if (!evaluateForm.activityId) {
    ElMessage.warning("请先选择一个活动进行评估");
    return;
  }
  evaluating.value = true;
  try {
    const response = await evaluateActivity(evaluateForm.activityId, {
      actual_student_count: Number(evaluateForm.actual_student_count),
      correct_match_count: Number(evaluateForm.correct_match_count),
      remark: evaluateForm.remark || null,
    });
    ElMessage.success("活动准确率评估已保存");
    if (latestResult.value && latestResult.value.activity_id === evaluateForm.activityId) {
      latestResult.value.evaluation_accuracy = response.data.accuracy;
    }
    await loadActivities();
    if (activityDetail.value && activityDetail.value.id === evaluateForm.activityId) {
      const detailResponse = await fetchActivityDetail(evaluateForm.activityId);
      activityDetail.value = detailResponse.data;
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "准确率评估失败");
  } finally {
    evaluating.value = false;
  }
}

async function handleExportActivity(activityId) {
  exporting.value = true;
  try {
    const response = await exportGroupPhotoActivity(activityId);
    const blob = new Blob([response.data], {
      type: response.headers["content-type"],
    });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    const disposition = response.headers["content-disposition"] || "";
    const match = disposition.match(/filename=\"?([^\"]+)\"?/);
    link.href = url;
    link.download = match?.[1] || `group_photo_activity_${activityId}.xlsx`;
    link.click();
    window.URL.revokeObjectURL(url);
    ElMessage.success("活动结果导出成功");
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "活动结果导出失败");
  } finally {
    exporting.value = false;
  }
}

function openCorrectionDialog(faceRow) {
  selectedFaceResult.value = faceRow;
  correctionForm.action = faceRow.status === "matched" ? "mark_unknown" : "assign_student";
  correctionForm.student_id = faceRow.student_id ?? null;
  correctionForm.note = "";
  correctionDialogVisible.value = true;
}

async function submitCorrection() {
  if (!activityDetail.value || !selectedFaceResult.value) {
    return;
  }
  if (correctionForm.action === "assign_student" && !correctionForm.student_id) {
    ElMessage.warning("请选择目标学生");
    return;
  }

  correcting.value = true;
  try {
    const response = await correctGroupPhotoFaceResult(
      activityDetail.value.id,
      selectedFaceResult.value.id,
      {
        action: correctionForm.action,
        student_id:
          correctionForm.action === "assign_student"
            ? Number(correctionForm.student_id)
            : null,
        note: correctionForm.note || null,
      }
    );
    activityDetail.value = response.data.activity;
    if (latestResult.value && latestResult.value.activity_id === activityDetail.value.id) {
      latestResult.value = {
        ...latestResult.value,
        face_count: activityDetail.value.face_count,
        matched_count: activityDetail.value.matched_count,
        unmatched_count: activityDetail.value.unmatched_count,
        participant_count: activityDetail.value.participant_count,
        participants: activityDetail.value.participants,
        unknown_faces: activityDetail.value.unknown_faces,
        all_faces: activityDetail.value.all_faces,
      };
    }
    await loadActivities();
    correctionDialogVisible.value = false;
    ElMessage.success("人工修正已保存");
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "人工修正失败");
  } finally {
    correcting.value = false;
  }
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

function goToReport() {
  router.push({ name: "report" });
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
  await Promise.all([loadActivities(), loadStudents()]);
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="合照识别" current="group-photos" :user="user" @logout="logout" />

    <section class="stats-grid">
      <article class="stat-card">
        <span>活动总数</span>
        <strong>{{ activityStats.total }}</strong>
      </article>
      <article class="stat-card success">
        <span>检测到的人脸</span>
        <strong>{{ activityStats.totalFaces }}</strong>
      </article>
      <article class="stat-card success">
        <span>匹配成功脸数</span>
        <strong>{{ activityStats.totalMatched }}</strong>
      </article>
      <article class="stat-card warning">
        <span>平均准确率</span>
        <strong>{{ activityStats.averageAccuracy }}</strong>
      </article>
    </section>

    <div class="capture-grid">
      <section class="panel">
        <div class="panel-head">
          <h2>上传活动合照</h2>
        </div>
        <el-form label-position="top">
          <div class="filters-grid">
            <el-form-item label="活动名称">
              <el-input v-model="uploadForm.title" placeholder="如：五一班级团建" />
            </el-form-item>
            <el-form-item label="活动类型">
              <el-select v-model="uploadForm.activityType">
                <el-option label="班级活动" value="class_activity" />
                <el-option label="讲座活动" value="lecture" />
                <el-option label="竞赛活动" value="competition" />
                <el-option label="团建活动" value="team_building" />
              </el-select>
            </el-form-item>
            <el-form-item label="活动日期">
              <el-date-picker
                v-model="uploadForm.activityDate"
                type="date"
                value-format="YYYY-MM-DD"
                placeholder="请选择日期"
              />
            </el-form-item>
          </div>

          <el-upload
            drag
            :auto-upload="false"
            :limit="1"
            accept=".jpg,.jpeg,.png,.bmp,.webp"
            :on-change="handlePhotoChange"
          >
            <div class="upload-placeholder">
              上传班级或活动合照，系统将检测并批量识别人脸。
            </div>
          </el-upload>
        </el-form>

        <div class="preview-card group-photo-preview">
          <span>合照预览</span>
          <img v-if="selectedPhotoPreview" :src="selectedPhotoPreview" alt="合照预览" />
          <div v-else class="empty-state">选择图片后将显示预览</div>
        </div>

        <div class="record-actions">
          <el-button type="primary" :loading="submitting" @click="submitGroupPhoto">
            开始识别
          </el-button>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <h2>最近一次识别结果</h2>
        </div>

        <div v-if="latestResult" class="result-card">
          <div class="result-grid">
            <div>
              <span>活动名称</span>
              <strong>{{ latestResult.title }}</strong>
            </div>
            <div>
              <span>活动日期</span>
              <strong>{{ latestResult.activity_date }}</strong>
            </div>
            <div>
              <span>总人脸数</span>
              <strong>{{ latestResult.face_count }}</strong>
            </div>
            <div>
              <span>匹配成功</span>
              <strong>{{ latestResult.matched_count }}</strong>
            </div>
            <div>
              <span>未匹配</span>
              <strong>{{ latestResult.unmatched_count }}</strong>
            </div>
            <div>
              <span>唯一参与人数</span>
              <strong>{{ latestResult.participant_count }}</strong>
            </div>
          </div>

          <div class="participants-block">
            <h3>参与名单</h3>
            <el-table :data="latestResult.participants" border stripe>
              <el-table-column prop="student_no" label="学号" width="120" />
              <el-table-column prop="student_name" label="姓名" width="110" />
              <el-table-column prop="class_name" label="班级" width="130" />
              <el-table-column prop="match_score" label="匹配分数" width="110" />
            </el-table>
          </div>
        </div>

        <div v-else class="empty-card">
          上传合照后，这里会显示识别统计和参与名单。
        </div>

        <div class="panel-tip">
          活动详情中支持导出 Excel 结果，并可对具体人脸执行人工修正。
        </div>
      </section>
    </div>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>准确率评估</h2>
      </div>
      <el-form label-position="top">
        <div class="filters-grid">
          <el-form-item label="活动 ID">
            <el-input v-model="evaluateForm.activityId" placeholder="可从活动记录点击“填入评估”" />
          </el-form-item>
          <el-form-item label="实际参与人数">
            <el-input v-model="evaluateForm.actual_student_count" placeholder="人工核验后的实际人数" />
          </el-form-item>
          <el-form-item label="正确识别人数">
            <el-input v-model="evaluateForm.correct_match_count" placeholder="人工核验后的正确识别人数" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="evaluateForm.remark" placeholder="可填写识别情况说明" />
          </el-form-item>
        </div>
        <div class="record-actions">
          <div class="inline-metric">
            <span>预计准确率</span>
            <strong>{{ expectedAccuracy ?? "-" }}</strong>
          </div>
          <el-button type="primary" :loading="evaluating" @click="submitEvaluation">
            保存准确率评估
          </el-button>
        </div>
      </el-form>
    </section>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>活动记录</h2>
        <div class="record-actions">
          <el-button @click="resetFilters">重置筛选</el-button>
          <el-button type="primary" @click="loadActivities">查询</el-button>
        </div>
      </div>

      <el-form class="filters-form" label-position="top">
        <div class="filters-grid">
          <el-form-item label="活动名称">
            <el-input v-model="filters.keyword" placeholder="按活动名称搜索" />
          </el-form-item>
          <el-form-item label="活动类型">
            <el-select v-model="filters.activity_type" clearable placeholder="全部">
              <el-option label="班级活动" value="class_activity" />
              <el-option label="讲座活动" value="lecture" />
              <el-option label="竞赛活动" value="competition" />
              <el-option label="团建活动" value="team_building" />
            </el-select>
          </el-form-item>
          <el-form-item label="活动日期">
            <el-date-picker
              v-model="filters.activity_date"
              type="date"
              value-format="YYYY-MM-DD"
              placeholder="按日期筛选"
            />
          </el-form-item>
        </div>
      </el-form>

      <el-table :data="activities" v-loading="loading" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="活动名称" min-width="180" />
        <el-table-column label="活动类型" width="140">
          <template #default="{ row }">
            <span>{{ formatActivityType(row.activity_type) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="activity_date" label="活动日期" width="120" />
        <el-table-column prop="face_count" label="人脸数" width="90" />
        <el-table-column prop="matched_count" label="匹配成功" width="100" />
        <el-table-column prop="participant_count" label="参与人数" width="90" />
        <el-table-column label="准确率" width="100">
          <template #default="{ row }">
            <span>
              {{
                row.evaluation_accuracy !== undefined && row.evaluation_accuracy !== null
                  ? row.evaluation_accuracy
                  : "-"
              }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" min-width="180" />
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button size="small" type="primary" @click="openActivityDetail(row)">
                查看详情
              </el-button>
              <el-button size="small" @click="fillEvaluationForm(row)">
                填入评估
              </el-button>
              <el-button size="small" type="success" @click="handleExportActivity(row.id)">
                导出结果
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <el-dialog v-model="detailDialogVisible" title="活动详情" width="1180px">
      <div v-loading="detailLoading">
        <div v-if="activityDetail" class="result-card">
          <div class="result-grid">
            <div>
              <span>活动名称</span>
              <strong>{{ activityDetail.title }}</strong>
            </div>
            <div>
              <span>活动类型</span>
              <strong>{{ formatActivityType(activityDetail.activity_type) }}</strong>
            </div>
            <div>
              <span>活动日期</span>
              <strong>{{ activityDetail.activity_date }}</strong>
            </div>
            <div>
              <span>总人脸数</span>
              <strong>{{ activityDetail.face_count }}</strong>
            </div>
            <div>
              <span>匹配成功</span>
              <strong>{{ activityDetail.matched_count }}</strong>
            </div>
            <div>
              <span>未匹配</span>
              <strong>{{ activityDetail.unmatched_count }}</strong>
            </div>
          </div>
<<<<<<< HEAD
=======

          <div class="detail-photo-block">
            <span>识别合照</span>
            <img
              v-if="activityDetail.image_path"
              :src="buildActivityImageUrl(activityDetail.image_path)"
              :alt="activityDetail.title || '活动合照'"
            />
            <div v-else class="empty-state">当前活动没有可显示的合照</div>
          </div>
>>>>>>> 98bf8e49 (update)
        </div>

        <div v-if="activityDetail" class="participants-block">
          <div class="detail-headline">
            <h3>全部人脸结果</h3>
            <el-button type="success" :loading="exporting" @click="handleExportActivity(activityDetail.id)">
              导出当前活动
            </el-button>
          </div>
          <el-table :data="activityDetail.all_faces" border stripe>
            <el-table-column prop="face_index" label="人脸序号" width="90" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="statusTagType(row.status)">
                  {{ formatStatus(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="student_no" label="学号" width="120" />
            <el-table-column prop="student_name" label="姓名" width="110" />
            <el-table-column prop="class_name" label="班级" width="120" />
            <el-table-column prop="match_score" label="匹配分数" width="110" />
            <el-table-column prop="det_score" label="检测分数" width="110" />
<<<<<<< HEAD
            <el-table-column prop="emotion" label="情绪" width="90" />
=======
            <el-table-column label="情绪" width="100">
              <template #default="{ row }">
                <span>{{ formatEmotion(row.emotion) }}</span>
              </template>
            </el-table-column>
>>>>>>> 98bf8e49 (update)
            <el-table-column prop="emotion_score" label="情绪分数" width="110" />
            <el-table-column label="人工修正" width="110">
              <template #default="{ row }">
                <el-tag :type="reviewTagType(row.manual_review_status)">
                  {{ row.manual_review_status === "reviewed" ? "已修正" : "原始结果" }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="修正动作" width="110">
              <template #default="{ row }">
                <span>{{ formatReviewAction(row.manual_review_action) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="manual_review_by" label="修正人" width="100" />
            <el-table-column prop="manual_review_at" label="修正时间" min-width="160" />
            <el-table-column prop="manual_review_note" label="备注" min-width="160" show-overflow-tooltip />
            <el-table-column label="操作" width="100" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="openCorrectionDialog(row)">修正</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>

        <div v-if="activityDetail" class="participants-block">
          <h3>唯一参与名单</h3>
          <el-table :data="activityDetail.participants" border stripe>
            <el-table-column prop="student_no" label="学号" width="120" />
            <el-table-column prop="student_name" label="姓名" width="110" />
            <el-table-column prop="class_name" label="班级" width="120" />
            <el-table-column prop="match_score" label="匹配分数" width="110" />
            <el-table-column prop="det_score" label="检测分数" width="110" />
          </el-table>
        </div>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="correctionDialogVisible" title="人工修正人脸结果" width="520px">
      <div v-if="selectedFaceResult" class="result-card correction-card">
        <div class="result-grid">
          <div>
            <span>人脸序号</span>
            <strong>{{ selectedFaceResult.face_index }}</strong>
          </div>
          <div>
            <span>当前状态</span>
            <strong>{{ formatStatus(selectedFaceResult.status) }}</strong>
          </div>
          <div>
            <span>当前学生</span>
            <strong>{{ selectedFaceResult.student_name || "-" }}</strong>
          </div>
          <div>
            <span>匹配分数</span>
            <strong>{{ selectedFaceResult.match_score }}</strong>
          </div>
        </div>
      </div>

      <el-form label-position="top">
        <el-form-item label="修正动作">
          <el-radio-group v-model="correctionForm.action">
            <el-radio value="assign_student">改派给学生</el-radio>
            <el-radio value="mark_unknown">改为未知人脸</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="correctionForm.action === 'assign_student'" label="目标学生">
          <el-select v-model="correctionForm.student_id" filterable placeholder="请选择学生">
            <el-option
              v-for="item in students"
              :key="item.id"
              :label="`${item.student_no} / ${item.name} / ${item.class_name}`"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="correctionForm.note"
            type="textarea"
            :rows="3"
            placeholder="可填写人工核验说明"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="correctionDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="correcting" @click="submitCorrection">
          保存修正
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.participants-block {
  margin-top: 22px;
}

.participants-block h3 {
  margin: 0 0 14px;
}

.detail-headline {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

<<<<<<< HEAD
=======
.detail-photo-block {
  margin-top: 18px;
}

.detail-photo-block span {
  display: block;
  margin-bottom: 10px;
  color: var(--text-soft);
}

.detail-photo-block img {
  display: block;
  width: 100%;
  max-height: 420px;
  object-fit: contain;
  border-radius: 20px;
  border: 1px solid var(--line);
  background: rgba(255, 250, 244, 0.72);
}

>>>>>>> 98bf8e49 (update)
.correction-card {
  margin-bottom: 18px;
}
</style>
