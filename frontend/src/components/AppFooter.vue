<template>
  <footer class="app-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <h3>🎸 BASS STUDIO</h3>
        <p>每一把贝斯，都是独一无二的艺术品</p>
      </div>
      <div class="footer-links">
        <div class="link-group">
          <h4>导航</h4>
          <router-link to="/">首页</router-link>
          <router-link to="/customize">定制贝斯</router-link>
          <router-link to="/login">登录</router-link>
        </div>
        <div class="link-group">
          <h4>联系</h4>
          <span>📧 info@bassstudio.com</span>
          <span>📞 +86 400-888-0000</span>
          <span>📍 上海市静安区南京西路 1688 号</span>
        </div>
        <div class="link-group">
          <h4>社交</h4>
          <a href="#">微信公众号</a>
          <a href="#">Bilibili</a>
          <a href="#">Instagram</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="container">
        <p>&copy; {{ year }} Bass Studio. All rights reserved. 仅供学习练习使用。</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>

<style scoped lang="scss">
.app-footer {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  margin-top: auto;
}

.footer-inner {
  display: flex;
  justify-content: space-between;
  gap: 48px;
  padding: 64px 20px 48px;
  flex-wrap: wrap;
}

.footer-brand {
  max-width: 300px;

  h3 {
    color: var(--accent);
    font-size: 1.2rem;
    margin-bottom: 12px;
    letter-spacing: 2px;
  }

  p {
    color: var(--text-muted);
    font-size: 0.9rem;
    line-height: 1.8;
  }
}

.footer-links {
  display: flex;
  gap: 64px;
  flex-wrap: wrap;
}

.link-group {
  display: flex;
  flex-direction: column;
  gap: 12px;

  h4 {
    color: var(--text-primary);
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }

  a, span {
    color: var(--text-muted);
    font-size: 0.85rem;
    transition: color 0.2s;
    text-decoration: none;
  }

  a:hover {
    color: var(--accent);
  }
}

.footer-bottom {
  border-top: 1px solid var(--border-color);
  padding: 20px 0;
  text-align: center;

  p {
    color: var(--text-muted);
    font-size: 0.8rem;
  }
}

@media (max-width: 768px) {
  .footer-inner {
    flex-direction: column;
    gap: 32px;
    padding: 40px 16px 32px;
  }

  .footer-links {
    gap: 32px;
  }
}
</style>
