<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";

import {
  bindStudentAccount,
  createStudent,
  deleteStudent,
  fetchStudents,
  importStudentsCsv,
  resetStudentAccountPassword,
  updateStudent,
  uploadStudentFace,
} from "../api/students";
import TeacherHeader from "../components/TeacherHeader.vue";
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();

const user = ref(null);
const loading = ref(false);
const submitting = ref(false);
const faceUploading = ref(false);
const importSubmitting = ref(false);

const students = ref([]);
const importResult = ref(null);
<<<<<<< HEAD
=======
const importCsvFile = ref(null);
const importPhotosZipFile = ref(null);
>>>>>>> 98bf8e49 (update)
const selectedFaceFile = ref(null);
const selectedFacePreview = ref("");
const selectedStudent = ref(null);
const faceUploadResult = ref(null);

const filters = reactive({
  keyword: "",
  class_name: "",
  is_active: "",
});

const formDialogVisible = ref(false);
const importDialogVisible = ref(false);
const faceDialogVisible = ref(false);
const formMode = ref("create");

const studentForm = reactive({
  student_no: "",
  name: "",
  class_name: "",
  is_active: true,
});

const studentStats = computed(() => {
  const total = students.value.length;
  const active = students.value.filter((item) => item.is_active).length;
  const ready = students.value.filter((item) => item.feature_status === "ready").length;
  const bound = students.value.filter((item) => item.account_bound).length;
  return { total, active, ready, bound };
});

function buildQuery() {
  return {
    keyword: filters.keyword || undefined,
    class_name: filters.class_name || undefined,
    is_active: filters.is_active === "" ? undefined : filters.is_active === "true",
  };
}

async function loadStudents() {
  loading.value = true;
  try {
    const response = await fetchStudents(buildQuery());
    students.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "学生列表加载失败");
  } finally {
    loading.value = false;
  }
}

function resetFilters() {
  filters.keyword = "";
  filters.class_name = "";
  filters.is_active = "";
  loadStudents();
}

<<<<<<< HEAD
function openCreateDialog() {
  formMode.value = "create";
=======
function buildFaceImageUrl(imagePath) {
  if (!imagePath) {
    return "";
  }
  if (imagePath.startsWith("http://") || imagePath.startsWith("https://")) {
    return imagePath;
  }
  return imagePath.startsWith("/") ? imagePath : `/${imagePath}`;
}

function openCreateDialog() {
  formMode.value = "create";
  selectedStudent.value = null;
>>>>>>> 98bf8e49 (update)
  studentForm.student_no = "";
  studentForm.name = "";
  studentForm.class_name = "";
  studentForm.is_active = true;
  formDialogVisible.value = true;
}

function openEditDialog(student) {
  formMode.value = "edit";
  selectedStudent.value = student;
  studentForm.student_no = student.student_no;
  studentForm.name = student.name;
  studentForm.class_name = student.class_name;
  studentForm.is_active = Boolean(student.is_active);
  formDialogVisible.value = true;
}

async function submitStudentForm() {
  submitting.value = true;
  try {
    if (formMode.value === "create") {
      const response = await createStudent({
        student_no: studentForm.student_no,
        name: studentForm.name,
        class_name: studentForm.class_name,
        is_active: studentForm.is_active,
      });
      ElMessage.success(
        `学生创建成功，账号 ${response.data.created_account_username}，初始密码 ${response.data.default_password}`
      );
    } else {
      await updateStudent(selectedStudent.value.id, {
        name: studentForm.name,
        class_name: studentForm.class_name,
        is_active: studentForm.is_active,
      });
      ElMessage.success("学生更新成功");
    }
    formDialogVisible.value = false;
    await loadStudents();
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "学生信息提交失败");
  } finally {
    submitting.value = false;
  }
}

async function handleDeleteStudent(student) {
  try {
    await ElMessageBox.confirm(
      `确定删除学生 ${student.name}（${student.student_no}）吗？该学生绑定的登录账号也会一并删除。`,
      "删除确认",
      {
        confirmButtonText: "删除",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    await deleteStudent(student.id);
    ElMessage.success("学生删除成功");
    await loadStudents();
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error(error.response?.data?.message || "学生删除失败");
    }
  }
}

async function handleBindAccount(student) {
  try {
    await ElMessageBox.confirm(
      `将为学生 ${student.name} 自动绑定账号，默认用户名为学号 ${student.student_no}，默认密码为 123456。是否继续？`,
      "绑定学生账号",
      {
        confirmButtonText: "继续",
        cancelButtonText: "取消",
        type: "info",
      }
    );
    const response = await bindStudentAccount(student.id, {});
    ElMessage.success(
      `绑定成功，账号 ${response.data.username}，密码 ${response.data.default_password}`
    );
    await loadStudents();
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error(error.response?.data?.message || "绑定学生账号失败");
    }
  }
}

async function handleResetPassword(student) {
  try {
    await ElMessageBox.confirm(
      `确定将 ${student.name} 的学生账号密码重置为 123456 吗？`,
      "重置密码",
      {
        confirmButtonText: "重置",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    const response = await resetStudentAccountPassword(student.id, {});
    ElMessage.success(
      `密码已重置，账号 ${response.data.username}，新密码 ${response.data.reset_password}`
    );
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error(error.response?.data?.message || "重置密码失败");
    }
  }
}

function handleImportFileChange(uploadFile) {
<<<<<<< HEAD
  selectedFaceFile.value = null;
  importResult.value = null;
  if (uploadFile?.raw) {
    importResult.value = { file: uploadFile.raw };
  }
}

async function submitImportCsv() {
  const file = importResult.value?.file;
=======
  importResult.value = null;
  importCsvFile.value = uploadFile?.raw || null;
}

function handleImportZipFileChange(uploadFile) {
  importResult.value = null;
  importPhotosZipFile.value = uploadFile?.raw || null;
}

async function submitImportCsv() {
  const file = importCsvFile.value;
>>>>>>> 98bf8e49 (update)
  if (!file) {
    ElMessage.warning("请先选择 CSV 文件");
    return;
  }

  importSubmitting.value = true;
  try {
<<<<<<< HEAD
    const response = await importStudentsCsv(file);
=======
    const response = await importStudentsCsv(file, importPhotosZipFile.value);
>>>>>>> 98bf8e49 (update)
    importResult.value = response.data;
    ElMessage.success(
      `批量导入完成，默认学生密码为 ${response.data.default_password}`
    );
    await loadStudents();
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "批量导入失败");
  } finally {
    importSubmitting.value = false;
  }
}

function openFaceDialog(student) {
  selectedStudent.value = student;
  selectedFaceFile.value = null;
  selectedFacePreview.value = "";
  faceUploadResult.value = null;
  faceDialogVisible.value = true;
}

function handleFaceFileChange(uploadFile) {
  if (!uploadFile?.raw) {
    selectedFaceFile.value = null;
    selectedFacePreview.value = "";
    return;
  }
  selectedFaceFile.value = uploadFile.raw;
  selectedFacePreview.value = URL.createObjectURL(uploadFile.raw);
}

async function submitFaceUpload() {
  if (!selectedStudent.value || !selectedFaceFile.value) {
    ElMessage.warning("请先选择学生并上传注册照");
    return;
  }

  faceUploading.value = true;
  try {
    const response = await uploadStudentFace(selectedStudent.value.id, selectedFaceFile.value);
    faceUploadResult.value = response.data;
    ElMessage.success("学生人脸注册成功");
    await loadStudents();
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "学生人脸注册失败");
  } finally {
    faceUploading.value = false;
  }
}

function goToAttendance() {
  router.push({ name: "attendance" });
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
  await loadStudents();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="学生管理" current="students" :user="user" @logout="logout" />

    <section class="stats-grid">
      <article class="stat-card">
        <span>学生总数</span>
        <strong>{{ studentStats.total }}</strong>
      </article>
      <article class="stat-card success">
        <span>启用学生</span>
        <strong>{{ studentStats.active }}</strong>
      </article>
      <article class="stat-card success">
        <span>特征就绪</span>
        <strong>{{ studentStats.ready }}</strong>
      </article>
      <article class="stat-card warning">
        <span>已绑定账号</span>
        <strong>{{ studentStats.bound }}</strong>
      </article>
    </section>

    <section class="panel">
      <div class="panel-head">
        <h2>学生筛选与管理</h2>
        <div class="record-actions">
          <el-button @click="resetFilters">重置筛选</el-button>
          <el-button type="primary" @click="loadStudents">查询</el-button>
          <el-button type="success" @click="openCreateDialog">新增学生</el-button>
          <el-button type="warning" @click="importDialogVisible = true">批量导入</el-button>
        </div>
      </div>

      <el-form class="filters-form" label-position="top">
        <div class="filters-grid">
          <el-form-item label="姓名/学号">
            <el-input v-model="filters.keyword" placeholder="按姓名或学号搜索" />
          </el-form-item>
          <el-form-item label="班级">
            <el-input v-model="filters.class_name" placeholder="如：信安1班" />
          </el-form-item>
          <el-form-item label="启用状态">
            <el-select v-model="filters.is_active" clearable placeholder="全部">
              <el-option label="启用" value="true" />
              <el-option label="停用" value="false" />
            </el-select>
          </el-form-item>
        </div>
      </el-form>

      <el-table :data="students" v-loading="loading" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="student_no" label="学号" width="130" />
        <el-table-column prop="name" label="姓名" width="110" />
        <el-table-column prop="class_name" label="班级" width="130" />
        <el-table-column label="学生状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="账号绑定" width="100">
          <template #default="{ row }">
            <el-tag :type="row.account_bound ? 'success' : 'warning'">
              {{ row.account_bound ? "已绑定" : "未绑定" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="account_username" label="学生账号" width="140" />
        <el-table-column label="账号状态" width="100">
          <template #default="{ row }">
            <span>{{ row.account_is_active === null ? "-" : row.account_is_active ? "启用" : "停用" }}</span>
          </template>
        </el-table-column>
        <el-table-column label="特征状态" width="110">
          <template #default="{ row }">
            <el-tag :type="row.feature_status === 'ready' ? 'success' : 'warning'">
              {{ row.feature_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="face_image_path" label="注册照路径" min-width="220" />
        <el-table-column prop="face_feature_path" label="特征路径" min-width="200" />
        <el-table-column prop="created_at" label="创建时间" min-width="170" />
        <el-table-column label="操作" width="420" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
              <el-button size="small" type="primary" @click="openFaceDialog(row)">
                注册人脸
              </el-button>
              <el-button
                size="small"
                type="success"
                @click="handleBindAccount(row)"
              >
                {{ row.account_bound ? "重新绑定" : "绑定账号" }}
              </el-button>
              <el-button
                size="small"
                type="warning"
                :disabled="!row.account_bound"
                @click="handleResetPassword(row)"
              >
                重置密码
              </el-button>
              <el-button size="small" type="danger" @click="handleDeleteStudent(row)">
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <el-dialog
      v-model="formDialogVisible"
      :title="formMode === 'create' ? '新增学生' : '编辑学生'"
      width="540px"
    >
      <el-form label-position="top">
<<<<<<< HEAD
=======
        <el-form-item v-if="formMode === 'edit'" label="人脸照片">
          <div class="preview-card edit-face-preview">
            <img
              v-if="selectedStudent?.face_image_path"
              :src="buildFaceImageUrl(selectedStudent.face_image_path)"
              :alt="`${selectedStudent.name || '学生'}注册照`"
            />
            <div v-else class="empty-state">未绑定</div>
          </div>
        </el-form-item>
>>>>>>> 98bf8e49 (update)
        <el-form-item label="学号">
          <el-input
            v-model="studentForm.student_no"
            :disabled="formMode === 'edit'"
            placeholder="请输入学号"
          />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="studentForm.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="班级">
          <el-input v-model="studentForm.class_name" placeholder="请输入班级" />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="studentForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitStudentForm">
          提交
        </el-button>
      </template>
    </el-dialog>

<<<<<<< HEAD
    <el-dialog v-model="importDialogVisible" title="批量导入学生" width="640px">
      <el-upload
        drag
        :auto-upload="false"
        :limit="1"
        accept=".csv"
        :on-change="handleImportFileChange"
      >
        <div class="upload-placeholder">
          上传 UTF-8 编码的 CSV，表头至少包含
          <strong>student_no,name,class_name</strong>
        </div>
      </el-upload>
=======
    <el-dialog v-model="importDialogVisible" title="批量导入学生" width="760px">
      <div class="face-upload-layout import-layout">
        <div class="face-upload-box">
          <h3>学生信息 CSV</h3>
          <el-upload
            drag
            :auto-upload="false"
            :limit="1"
            accept=".csv"
            :on-change="handleImportFileChange"
          >
            <div class="upload-placeholder">
              上传 UTF-8 编码的 CSV，表头至少包含
              <strong>student_no,name,class_name</strong>
            </div>
          </el-upload>
        </div>

        <div class="face-upload-box">
          <h3>学生照片 ZIP（可选）</h3>
          <el-upload
            drag
            :auto-upload="false"
            :limit="1"
            accept=".zip"
            :on-change="handleImportZipFileChange"
          >
            <div class="upload-placeholder">
              上传 ZIP 压缩包，照片文件名请使用学号命名，例如
              <strong>20240001.jpg</strong>
            </div>
          </el-upload>
        </div>
      </div>
>>>>>>> 98bf8e49 (update)

      <div v-if="importResult && importResult.created_count !== undefined" class="import-summary">
        <p>创建成功：{{ importResult.created_count }}</p>
        <p>跳过数量：{{ importResult.skipped_count }}</p>
<<<<<<< HEAD
        <p>默认学生密码：{{ importResult.default_password }}</p>
        <div v-if="importResult.skipped?.length" class="skipped-list">
          <strong>跳过明细</strong>
          <ul>
            <li v-for="item in importResult.skipped" :key="`${item.row}-${item.reason}`">
=======
        <p>成功绑定照片：{{ importResult.photo_bound_count }}</p>
        <p>缺失照片：{{ importResult.photo_missing_count }}</p>
        <p>照片处理失败：{{ importResult.photo_failed_count }}</p>
        <p>ZIP 未匹配照片：{{ importResult.unmatched_photo_count }}</p>
        <p>ZIP 重复学号照片：{{ importResult.duplicate_photo_count }}</p>
        <p>默认学生密码：{{ importResult.default_password }}</p>

        <div v-if="importResult.skipped?.length" class="skipped-list">
          <strong>跳过明细</strong>
          <ul>
            <li v-for="item in importResult.skipped" :key="`skip-${item.row}-${item.reason}`">
>>>>>>> 98bf8e49 (update)
              第 {{ item.row }} 行：{{ item.reason }}
            </li>
          </ul>
        </div>
<<<<<<< HEAD
=======

        <div v-if="importResult.photo_missing?.length" class="skipped-list">
          <strong>缺失照片</strong>
          <ul>
            <li
              v-for="item in importResult.photo_missing"
              :key="`missing-${item.row}-${item.student_no}`"
            >
              第 {{ item.row }} 行 / 学号 {{ item.student_no }}：{{ item.reason }}
            </li>
          </ul>
        </div>

        <div v-if="importResult.photo_failed?.length" class="skipped-list">
          <strong>照片处理失败</strong>
          <ul>
            <li
              v-for="item in importResult.photo_failed"
              :key="`failed-${item.row}-${item.student_no}-${item.reason}`"
            >
              第 {{ item.row }} 行 / 学号 {{ item.student_no }}：{{ item.reason }}
            </li>
          </ul>
        </div>

        <div v-if="importResult.unmatched_photos?.length" class="skipped-list">
          <strong>ZIP 中未匹配到学生的照片</strong>
          <ul>
            <li
              v-for="item in importResult.unmatched_photos"
              :key="`unmatched-${item.student_no}-${item.filename}`"
            >
              {{ item.filename }}（识别学号：{{ item.student_no }}）
            </li>
          </ul>
        </div>

        <div v-if="importResult.duplicate_photos?.length" class="skipped-list">
          <strong>ZIP 中重复学号照片</strong>
          <ul>
            <li
              v-for="item in importResult.duplicate_photos"
              :key="`duplicate-${item.student_no}`"
            >
              学号 {{ item.student_no }}：{{ item.filenames.join("、") }}
            </li>
          </ul>
        </div>
>>>>>>> 98bf8e49 (update)
      </div>

      <template #footer>
        <el-button @click="importDialogVisible = false">关闭</el-button>
        <el-button type="primary" :loading="importSubmitting" @click="submitImportCsv">
          开始导入
        </el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="faceDialogVisible" title="学生人脸注册" width="720px">
      <div class="face-upload-layout">
        <div class="face-upload-box">
          <h3>
            {{
              selectedStudent
                ? `${selectedStudent.name}（${selectedStudent.student_no}）`
                : "请选择学生"
            }}
          </h3>
          <el-upload
            drag
            :auto-upload="false"
            :limit="1"
            accept=".jpg,.jpeg,.png,.bmp,.webp"
            :on-change="handleFaceFileChange"
          >
            <div class="upload-placeholder">上传单人正面注册照，用于提取人脸特征</div>
          </el-upload>

          <div class="preview-card">
            <span>图片预览</span>
            <img v-if="selectedFacePreview" :src="selectedFacePreview" alt="注册照预览" />
            <div v-else class="empty-state">上传图片后将在此显示预览</div>
          </div>
        </div>

        <div class="face-upload-box">
          <h3>提取结果</h3>
          <div v-if="faceUploadResult" class="result-card">
            <div class="result-grid">
              <div>
                <span>学号</span>
                <strong>{{ faceUploadResult.student_no }}</strong>
              </div>
              <div>
                <span>特征状态</span>
                <strong>{{ faceUploadResult.feature_status }}</strong>
              </div>
              <div>
                <span>检测分数</span>
                <strong>{{ faceUploadResult.det_score }}</strong>
              </div>
              <div>
                <span>特征维度</span>
                <strong>{{ faceUploadResult.embedding_dim }}</strong>
              </div>
              <div>
                <span>注册照路径</span>
                <strong>{{ faceUploadResult.face_image_path }}</strong>
              </div>
              <div>
                <span>特征路径</span>
                <strong>{{ faceUploadResult.face_feature_path }}</strong>
              </div>
            </div>
          </div>
          <div v-else class="empty-card">上传注册照后，这里会显示检测与特征提取结果。</div>
        </div>
      </div>

      <template #footer>
        <el-button @click="faceDialogVisible = false">关闭</el-button>
        <el-button type="primary" :loading="faceUploading" @click="submitFaceUpload">
          上传并提取特征
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>
<<<<<<< HEAD
=======

<style scoped>
.edit-face-preview {
  margin-top: 0;
}

.edit-face-preview img {
  display: block;
  width: 100%;
  max-height: 260px;
  object-fit: contain;
  border-radius: 18px;
}
</style>
>>>>>>> 98bf8e49 (update)
