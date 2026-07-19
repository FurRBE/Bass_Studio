<template>
  <DefaultLayout>
    <!-- Hero 区域 -->
    <section class="hero">
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <h1 class="hero-title">打造你的专属贝斯</h1>
        <p class="hero-subtitle">
          从木材到拾音器，从漆面到琴桥 —— 每一个细节，都由你决定。
          <br />Bass Studio 为你呈现真正的手工定制体验。
        </p>
        <div class="hero-actions">
          <router-link to="/customize">
            <el-button type="primary" size="large" round class="cta-btn">
              开始定制
            </el-button>
          </router-link>
          <el-button size="large" round class="ghost-btn" @click="scrollToIntro">
            了解更多
          </el-button>
        </div>
      </div>
    </section>

    <!-- 工作室介绍 -->
    <section id="intro" class="section intro-section">
      <div class="container">
        <h2 class="section-title">关于我们</h2>
        <div class="section-divider"></div>
        <div class="intro-grid">
          <div class="intro-text">
            <p>
              Bass Studio 成立于 2018 年，由一群热爱贝斯的手工匠人创立。
              我们相信每一把贝斯都应该像它的主人一样独一无二。
            </p>
            <p>
              从选材到制作，从调校到交付，我们坚持手工打造每一个环节。
              使用来自世界各地的优质木材和顶级电子元件，为每一位音乐人
              创造属于他们的声音。
            </p>
            <div class="intro-stats">
              <div class="stat">
                <span class="stat-number">500+</span>
                <span class="stat-label">定制贝斯</span>
              </div>
              <div class="stat">
                <span class="stat-number">30+</span>
                <span class="stat-label">城市覆盖</span>
              </div>
              <div class="stat">
                <span class="stat-number">98%</span>
                <span class="stat-label">客户好评</span>
              </div>
            </div>
          </div>
          <div class="intro-image">
            <div class="image-placeholder">
              <span>🎸</span>
              <p>手工定制贝斯</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 定制流程 -->
    <section class="section process-section">
      <div class="container">
        <h2 class="section-title">定制流程</h2>
        <div class="section-divider"></div>
        <div class="process-grid">
          <div class="process-card" v-for="(step, idx) in processSteps" :key="idx">
            <div class="process-number">{{ String(idx + 1).padStart(2, '0') }}</div>
            <div class="process-icon">{{ step.icon }}</div>
            <h3>{{ step.title }}</h3>
            <p>{{ step.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 精选展示 -->
    <section class="section showcase-section">
      <div class="container">
        <h2 class="section-title">精选作品</h2>
        <div class="section-divider"></div>
        <div class="showcase-grid">
          <div class="showcase-card" v-for="bass in showcaseBasses" :key="bass.name">
            <div class="showcase-image">
              <span class="showcase-icon">🎸</span>
            </div>
            <div class="showcase-info">
              <h3>{{ bass.name }}</h3>
              <p>{{ bass.spec }}</p>
              <span class="showcase-price">¥{{ bass.price.toLocaleString() }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA 区域 -->
    <section class="section cta-section">
      <div class="container cta-content">
        <h2>准备好打造你的专属贝斯了吗？</h2>
        <p>从选择第一块木材开始，创造只属于你的声音。</p>
        <router-link to="/customize">
          <el-button type="primary" size="large" round>立即开始定制</el-button>
        </router-link>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup lang="ts">
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const processSteps = [
  { icon: '🎯', title: '选择配置', desc: '在线选择你喜欢的木材、拾音器、颜色等各项配置' },
  { icon: '📋', title: '确认订单', desc: '提交订单后，我们的工匠会审核配置并与你确认细节' },
  { icon: '🔨', title: '手工制作', desc: '经验丰富的工匠开始手工打造，每个环节精益求精' },
  { icon: '🎵', title: '调校交付', desc: '专业调校后安全包装，送到你的手中' },
]

const showcaseBasses = [
  { name: 'Classic J-Style', spec: '赤杨木琴体 · 枫木琴颈 · 玫瑰木指板', price: 8900 },
  { name: 'Modern P-Style', spec: '桃花心木琴体 · 烘烤枫木琴颈 · 乌木指板', price: 12800 },
  { name: 'Custom 5-String', spec: '水曲柳琴体 · 鸡翅木琴颈 · 乌木指板', price: 15600 },
]

function scrollToIntro() {
  document.getElementById('intro')?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<style scoped lang="scss">
// Hero
.hero {
  position: relative;
  min-height: 90vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #0d0d0d 0%, #1a1410 40%, #0d0d0d 100%);
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 800px;
    height: 800px;
    background: radial-gradient(circle, rgba(200, 164, 92, 0.08) 0%, transparent 70%);
    border-radius: 50%;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(200, 164, 92, 0.05) 0%, transparent 70%);
    border-radius: 50%;
  }
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 2px,
      rgba(255,255,255,0.01) 2px,
      rgba(255,255,255,0.01) 4px
    );
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 120px 20px;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(180deg, var(--accent-light) 0%, var(--accent) 50%, var(--accent-dark) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 24px;
  letter-spacing: 4px;
}

.hero-subtitle {
  font-size: 1.15rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto 40px;
  line-height: 1.8;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-btn {
  padding: 14px 40px !important;
  font-size: 1rem !important;
  letter-spacing: 2px;
}

.ghost-btn {
  padding: 14px 40px !important;
  font-size: 1rem !important;
  background: transparent !important;
  border: 1px solid var(--border-light) !important;
  color: var(--text-secondary) !important;

  &:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
  }
}

// Intro
.intro-section {
  background: var(--bg-primary);
}

.intro-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 64px;
  align-items: center;
}

.intro-text {
  p {
    color: var(--text-secondary);
    line-height: 1.9;
    margin-bottom: 16px;
    font-size: 0.95rem;
  }
}

.intro-stats {
  display: flex;
  gap: 40px;
  margin-top: 32px;

  .stat {
    display: flex;
    flex-direction: column;

    .stat-number {
      font-size: 2rem;
      font-weight: 700;
      color: var(--accent);
    }

    .stat-label {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 4px;
    }
  }
}

.intro-image {
  .image-placeholder {
    aspect-ratio: 4/3;
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-hover) 100%);
    border-radius: 16px;
    border: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 16px;

    span {
      font-size: 4rem;
    }

    p {
      color: var(--text-muted);
      font-size: 0.9rem;
    }
  }
}

// Process
.process-section {
  background: var(--bg-secondary);
}

.process-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.process-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;

  &:hover {
    border-color: var(--accent);
    transform: translateY(-4px);

    .process-number {
      color: var(--accent);
    }
  }

  .process-number {
    position: absolute;
    top: 16px;
    right: 20px;
    font-size: 2.5rem;
    font-weight: 800;
    color: rgba(200, 164, 92, 0.1);
    transition: color 0.3s;
  }

  .process-icon {
    font-size: 2.5rem;
    margin-bottom: 16px;
  }

  h3 {
    color: var(--text-primary);
    font-size: 1.05rem;
    margin-bottom: 8px;
  }

  p {
    color: var(--text-muted);
    font-size: 0.85rem;
    line-height: 1.6;
  }
}

// Showcase
.showcase-section {
  background: var(--bg-primary);
}

.showcase-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.showcase-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;

  &:hover {
    border-color: var(--accent);
    transform: translateY(-4px);
  }

  .showcase-image {
    aspect-ratio: 16/10;
    background: linear-gradient(135deg, #1a1410, #1a1a1a);
    display: flex;
    align-items: center;
    justify-content: center;

    .showcase-icon {
      font-size: 4rem;
      opacity: 0.6;
    }
  }

  .showcase-info {
    padding: 20px;

    h3 {
      color: var(--text-primary);
      font-size: 1rem;
      margin-bottom: 8px;
    }

    p {
      color: var(--text-muted);
      font-size: 0.85rem;
      margin-bottom: 12px;
    }

    .showcase-price {
      color: var(--accent);
      font-weight: 700;
      font-size: 1.1rem;
    }
  }
}

// CTA
.cta-section {
  background: var(--bg-secondary);
  text-align: center;
}

.cta-content {
  padding: 60px 20px;

  h2 {
    font-size: 2rem;
    color: var(--text-primary);
    margin-bottom: 16px;
  }

  p {
    color: var(--text-secondary);
    margin-bottom: 32px;
  }
}

// Responsive
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
    letter-spacing: 2px;
  }

  .hero-subtitle {
    font-size: 0.95rem;
  }

  .intro-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .process-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .showcase-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .process-grid {
    grid-template-columns: 1fr;
  }
}
</style>
