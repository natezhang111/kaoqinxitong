<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";

import {
  createUser,
  deleteUser,
  fetchPermissionMatrix,
  fetchUsers,
  resetUserPassword,
  updateUser,
} from "../api/users";
import TeacherHeader from "../components/TeacherHeader.vue";
import { parseSavedUser, performLogout } from "../utils/session";

const router = useRouter();

const user = ref(null);
const loading = ref(false);
const submitting = ref(false);
const users = ref([]);
const permissionMatrix = ref([]);

const filters = reactive({
  keyword: "",
  role: "",
  is_active: "",
});

const createDialogVisible = ref(false);
const editDialogVisible = ref(false);
const selectedUser = ref(null);

const createForm = reactive({
  username: "",
  password: "123456",
  is_active: true,
});

const editForm = reactive({
  username: "",
  is_active: true,
});

const userStats = computed(() => {
  const total = users.value.length;
  const teachers = users.value.filter((item) => item.role === "teacher").length;
  const students = users.value.filter((item) => item.role === "student").length;
  const active = users.value.filter((item) => item.is_active).length;
  return { total, teachers, students, active };
});

function buildQuery() {
  return {
    keyword: filters.keyword || undefined,
    role: filters.role || undefined,
    is_active: filters.is_active === "" ? undefined : filters.is_active === "true",
  };
}

function formatRole(value) {
  return value === "teacher" ? "教师" : value === "student" ? "学生" : value || "-";
}

function sourceLabel(row) {
  return row.account_source === "student_binding" ? "学生绑定" : "独立账号";
}

async function loadUsers() {
  loading.value = true;
  try {
    const response = await fetchUsers(buildQuery());
    users.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "用户列表加载失败");
  } finally {
    loading.value = false;
  }
}

async function loadPermissionMatrix() {
  try {
    const response = await fetchPermissionMatrix();
    permissionMatrix.value = response.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "权限矩阵加载失败");
  }
}

async function refreshAll() {
  await Promise.all([loadUsers(), loadPermissionMatrix()]);
}

function resetFilters() {
  filters.keyword = "";
  filters.role = "";
  filters.is_active = "";
  loadUsers();
}

function openCreateDialog() {
  createForm.username = "";
  createForm.password = "123456";
  createForm.is_active = true;
  createDialogVisible.value = true;
}

function openEditDialog(row) {
  selectedUser.value = row;
  editForm.username = row.username || "";
  editForm.is_active = Boolean(row.is_active);
  editDialogVisible.value = true;
}

async function submitCreate() {
  if (!createForm.username.trim()) {
    ElMessage.warning("请输入用户名");
    return;
  }
  if (createForm.password.length < 6) {
    ElMessage.warning("初始密码长度不能少于 6 位");
    return;
  }

  submitting.value = true;
  try {
    await createUser({
      username: createForm.username.trim(),
      password: createForm.password,
      role: "teacher",
      is_active: createForm.is_active,
    });
    ElMessage.success("教师账号创建成功");
    createDialogVisible.value = false;
    await loadUsers();
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "创建用户失败");
  } finally {
    submitting.value = false;
  }
}

async function submitEdit() {
  if (!selectedUser.value) return;
  if (!editForm.username.trim() && selectedUser.value.can_edit_username) {
    ElMessage.warning("请输入用户名");
    return;
  }

  const payload = {
    is_active: editForm.is_active,
  };
  if (selectedUser.value.can_edit_username) {
    payload.username = editForm.username.trim();
  }

  submitting.value = true;
  try {
    await updateUser(selectedUser.value.id, payload);
    ElMessage.success("用户信息更新成功");
    editDialogVisible.value = false;
    await loadUsers();
  } catch (error) {
    ElMessage.error(error.response?.data?.message || "更新用户失败");
  } finally {
    submitting.value = false;
  }
}

async function handleResetPassword(row) {
  try {
    const { value } = await ElMessageBox.prompt(
      `请输入用户 ${row.username} 的新密码`,
      "重置密码",
      {
        confirmButtonText: "重置",
        cancelButtonText: "取消",
        inputValue: "123456",
        inputType: "password",
        inputPlaceholder: "请输入新密码",
      }
    );
    await resetUserPassword(row.id, { password: value });
    ElMessage.success(`密码重置成功，新密码为 ${value}`);
  } catch (error) {
    if (error !== "cancel" && error !== "close") {
      ElMessage.error(error.response?.data?.message || "重置密码失败");
    }
  }
}

async function handleDeleteUser(row) {
  try {
    await ElMessageBox.confirm(
      `确定删除用户 ${row.username} 吗？该操作不可恢复。`,
      "删除确认",
      {
        confirmButtonText: "删除",
        cancelButtonText: "取消",
        type: "warning",
      }
    );
    await deleteUser(row.id);
    ElMessage.success("用户删除成功");
    await loadUsers();
  } catch (error) {
    if (error !== "cancel" && error !== "close") {
      ElMessage.error(error.response?.data?.message || "删除用户失败");
    }
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

function goToGroupPhotos() {
  router.push({ name: "group-photos" });
}

function goToEmotions() {
  router.push({ name: "emotions" });
}

function goToReport() {
  router.push({ name: "report" });
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
  await refreshAll();
});
</script>

<template>
  <div class="page-shell">
    <TeacherHeader title="用户管理" current="users" :user="user" @logout="logout" />

    <section class="stats-grid">
      <article class="stat-card">
        <span>账号总数</span>
        <strong>{{ userStats.total }}</strong>
      </article>
      <article class="stat-card success">
        <span>教师账号</span>
        <strong>{{ userStats.teachers }}</strong>
      </article>
      <article class="stat-card success">
        <span>学生账号</span>
        <strong>{{ userStats.students }}</strong>
      </article>
      <article class="stat-card warning">
        <span>启用账号</span>
        <strong>{{ userStats.active }}</strong>
      </article>
    </section>

    <div class="capture-grid admin-grid">
      <section class="panel">
        <div class="panel-head">
          <h2>角色权限说明</h2>
        </div>
        <div class="permission-grid">
          <article
            v-for="item in permissionMatrix"
            :key="item.role"
            class="permission-card"
          >
            <span class="permission-role">{{ item.label }}</span>
            <strong>{{ item.role }}</strong>
            <ul>
              <li v-for="permission in item.permissions" :key="permission">
                {{ permission }}
              </li>
            </ul>
          </article>
        </div>
      </section>

      <section class="panel">
        <div class="panel-head">
          <h2>管理规则</h2>
        </div>
        <div class="panel-tip">
          当前页用于管理教师账号及查看所有账号状态。已绑定学生档案的学生账号，用户名绑定关系请优先在“学生管理”页维护。
        </div>
        <div class="result-card">
          <div class="result-grid">
            <div>
              <span>创建新账号</span>
              <strong>仅教师账号</strong>
            </div>
            <div>
              <span>学生账号来源</span>
              <strong>学生模块自动绑定</strong>
            </div>
            <div>
              <span>默认建议密码</span>
              <strong>123456</strong>
            </div>
            <div>
              <span>删除限制</span>
              <strong>不能删除当前登录账号</strong>
            </div>
          </div>
        </div>
      </section>
    </div>

    <section class="panel security-panel-gap">
      <div class="panel-head">
        <h2>用户筛选与管理</h2>
        <div class="record-actions">
          <el-button @click="resetFilters">重置筛选</el-button>
          <el-button type="primary" @click="loadUsers">查询</el-button>
          <el-button type="success" @click="openCreateDialog">新增教师账号</el-button>
        </div>
      </div>

      <el-form class="filters-form" label-position="top">
        <div class="filters-grid">
          <el-form-item label="用户名">
            <el-input v-model="filters.keyword" placeholder="按用户名搜索" />
          </el-form-item>
          <el-form-item label="角色">
            <el-select v-model="filters.role" clearable placeholder="全部">
              <el-option label="教师" value="teacher" />
              <el-option label="学生" value="student" />
            </el-select>
          </el-form-item>
          <el-form-item label="启用状态">
            <el-select v-model="filters.is_active" clearable placeholder="全部">
              <el-option label="启用" value="true" />
              <el-option label="停用" value="false" />
            </el-select>
          </el-form-item>
        </div>
      </el-form>

      <el-table :data="users" v-loading="loading" border stripe>
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="username" label="用户名" min-width="150" />
        <el-table-column label="角色" width="100">
          <template #default="{ row }">
            <el-tag :type="row.role === 'teacher' ? 'success' : 'warning'">
              {{ formatRole(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="账号来源" width="110">
          <template #default="{ row }">
            <span>{{ sourceLabel(row) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="学生关联信息" min-width="190">
          <template #default="{ row }">
            <span v-if="row.student">
              {{ row.student.student_no }} / {{ row.student.name }} / {{ row.student.class_name }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" min-width="170" />
        <el-table-column label="操作" width="290" fixed="right">
          <template #default="{ row }">
            <div class="table-actions">
              <el-button size="small" @click="openEditDialog(row)">编辑</el-button>
              <el-button size="small" type="warning" @click="handleResetPassword(row)">
                重置密码
              </el-button>
              <el-button
                size="small"
                type="danger"
                :disabled="!row.can_delete || row.id === user?.id"
                @click="handleDeleteUser(row)"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </section>

    <el-dialog v-model="createDialogVisible" title="新增教师账号" width="480px">
      <el-form label-position="top">
        <el-form-item label="用户名">
          <el-input v-model="createForm.username" placeholder="请输入教师用户名" />
        </el-form-item>
        <el-form-item label="初始密码">
          <el-input
            v-model="createForm.password"
            type="password"
            show-password
            placeholder="请输入初始密码"
          />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="createForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitCreate">
          创建
        </el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="editDialogVisible" title="编辑用户" width="480px">
      <el-form label-position="top">
        <el-form-item label="用户名">
          <el-input
            v-model="editForm.username"
            :disabled="!selectedUser?.can_edit_username"
            placeholder="请输入用户名"
          />
        </el-form-item>
        <el-form-item label="是否启用">
          <el-switch v-model="editForm.is_active" />
        </el-form-item>
        <div v-if="selectedUser?.linked_student" class="panel-tip">
          当前账号已绑定学生档案，用户名维护建议前往“学生管理”页操作。
        </div>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submitEdit">
          保存
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.admin-grid {
  grid-template-columns: 1.1fr 0.9fr;
}

.permission-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.permission-card {
  padding: 18px;
  border-radius: 22px;
  border: 1px solid var(--line);
  background: rgba(255, 250, 244, 0.72);
}

.permission-role {
  display: inline-flex;
  margin-bottom: 8px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(200, 100, 59, 0.12);
  color: var(--brand-deep);
  font-size: 12px;
}

.permission-card strong {
  display: block;
  margin-bottom: 10px;
  font-size: 1.05rem;
}

.permission-card ul {
  margin: 0;
  padding-left: 18px;
  color: var(--muted);
  line-height: 1.7;
}

@media (max-width: 960px) {
  .permission-grid {
    grid-template-columns: 1fr;
  }
}
</style>
