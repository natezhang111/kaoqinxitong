<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

import { login } from "../api/auth";

const router = useRouter();
const submitting = ref(false);

const form = reactive({
  username: "teacher",
  password: "123456",
});

async function handleLogin() {
  submitting.value = true;
  try {
    const result = await login(form);
    localStorage.setItem("attendance_token", result.data.access_token);
    localStorage.setItem("attendance_user", JSON.stringify(result.data.user));
    ElMessage.success("登录成功");
    router.push({
      name: result.data.user.role === "student" ? "student-portal" : "attendance",
    });
  } catch (error) {
    const message = error.response?.data?.message || "登录失败";
    ElMessage.error(message);
  } finally {
    submitting.value = false;
  }
}
</script>

<template>
  <div class="login-shell">
    <div class="login-panel">
      <div class="hero-copy">
        <p class="eyebrow">Attendance Content Security</p>
        <h1>考勤系统登录台</h1>
        <p class="subcopy">
          教师可进入管理端执行考勤、学生管理、合照识别与统计报表；学生可进入个人中心查看自己的考勤、活动与情绪记录。
        </p>
      </div>

      <el-form class="login-form" label-position="top" @submit.prevent="handleLogin">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            show-password
            placeholder="请输入密码"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-button class="solid-button" :loading="submitting" type="primary" @click="handleLogin">
          进入系统
        </el-button>
      </el-form>
    </div>
  </div>
</template>
