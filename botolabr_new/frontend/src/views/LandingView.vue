<template>
  <div class="landing">

    <!-- HEADER -->
    <header class="header">
      <div class="header__row">
        <div class="logo">
          <img src="\icons.svg" alt="BOTOLABR" @error="e => e.target.style.display='none'" />
          <span class="logo__fallback">BOTOLаBR</span>
        </div>

        <!-- Бургер для мобильных -->
        <button class="burger" @click="menuOpen = !menuOpen" :class="{ open: menuOpen }">
          <span></span><span></span><span></span>
        </button>

        <div class="header__buttons" :class="{ 'header__buttons--open': menuOpen }">
          <button class="btn btn--outline" @click="goToLogin('login')">Вход</button>
          <button class="btn btn--solid"   @click="goToLogin('register')">Регистрация</button>
        </div>
      </div>
    </header>

    <!-- HERO -->
    <section class="hero">
      <div class="hero__row">
        <div class="hero__text">
          <h1>botolabr</h1>
        </div>
        <div class="hero__konstruktor">Конструктор</div>
        <div class="hero__dlya">для</div>
        <div class="hero__chatbotov">Чат-ботов</div>
        <div class="hero__image">
          <img src="\doctor.png" alt="Doctor" @error="e => e.target.style.display='none'" />
        </div>
      </div>
    </section>

    <!-- VARIANT -->
    <section class="variant">
      <div class="variant__header">
        <div class="variant__text">
          <h1>Варианты использования чат-ботов</h1>
        </div>
        <div class="variant__description">
          Вы способны разработать бота для взаимодействия с покупателями в любой отрасли.<br class="br-desktop"/>
          В Botolabr представлены шаблоны надежных, эффективных моделей чат-ботов, адаптированных под разнообразные направления коммерции и задачи.<br class="br-desktop"/>
          Применяйте их для оптимизации процессов и ускорения достижения целей.
        </div>
      </div>

      <div class="variant__tabs">
        <div
          v-for="tab in variantTabs"
          :key="tab.id"
          class="tab"
          :class="{ active: activeVariant === tab.id }"
          @click="activeVariant = tab.id"
        >
          <img class="tab__icon" :src="tab.icon" :alt="tab.label" @error="e => e.target.style.display='none'" />
          <span>{{ tab.label }}</span>
        </div>
      </div>

      <div class="variant__contents">
        <transition name="tab-fade" mode="out-in">
          <div class="variant__content active" :key="activeVariant">
            <div class="variant__content-wrapper">
              <div class="variant__content-text">
                <p>{{ currentVariant.text1 }}</p>
                <p>{{ currentVariant.text2 }}</p>
                <button class="btn btn--variant" @click="goToLogin('register')">Попробуйте бесплатно</button>
              </div>
              <div
                class="variant__content-image"
                :style="{ backgroundImage: `url('${currentVariant.image}')` }"
              ></div>
            </div>
          </div>
        </transition>
      </div>
    </section>

    <!-- VOZMOZHNOST -->
    <section class="vozmozhnost">
      <div class="vozmozhnost__header">
        <div class="vozmozhnost__text">
          <h1>Возможности чат-ботов</h1>
        </div>
      </div>

      <div class="vozmozhnost__tabs">
        <div
          v-for="tab in vozmozhnostTabs"
          :key="tab.id"
          class="tab1"
          :class="{ active: activeVoz === tab.id }"
          @click="activeVoz = tab.id"
        >
          <img class="tab1__icon" :src="tab.icon" :alt="tab.label" @error="e => e.target.style.display='none'" />
          <span>{{ tab.label }}</span>
        </div>
      </div>

      <div class="vozmozhnost__contents">
        <transition name="tab-fade" mode="out-in">
          <div class="vozmozhnost__content active" :key="activeVoz">
            <div class="vozmozhnost__content-wrapper">
              <div
                class="vozmozhnost__content-image"
                :style="{ backgroundImage: `url('${currentVoz.image}')` }"
              ></div>
              <div class="vozmozhnost__content-right">
                <div class="vozmozhnost__description">{{ currentVoz.desc }}</div>
                <div class="vozmozhnost__content-text">
                  <p>{{ currentVoz.text }}</p>
                </div>
                <ul class="vozmozhnost__list">
                  <li v-for="item in currentVoz.list" :key="item">{{ item }}</li>
                </ul>
                <button class="btn btn--vozmozhnost" @click="goToLogin('register')">Попробуйте бесплатно</button>
              </div>
            </div>
          </div>
        </transition>
      </div>
    </section>

    <!-- О НАС -->
    <section class="about">
      <div class="about__inner">
        <h2 class="about__title">О нас</h2>
        <p class="about__text">Мы верим, что технологии должны быть простыми и доступными каждому.</p>
        <p class="about__text">Наша цель — упростить создание чат-ботов, чтобы предприниматели и команды могли сосредоточиться на росте, а не на технических сложностях.</p>
        <p class="about__text">Мы заботимся о стабильности, безопасности и поддержке наших пользователей.</p>
        <button class="btn btn--about" @click="goToLogin('register')">Попробуйте бесплатно</button>
      </div>
    </section>

    <!-- КАК МЫ РАБОТАЕМ -->
    <section class="how">
      <h2 class="how__title">
        Вот как конструктор чат<br/>
        ботов <span>Botolabr</span> поможет вам экономить<br/>
        время, деньги и быстрее развивать бизнес
      </h2>
      <div class="how__grid">
        <div class="how__card" v-for="card in howCards" :key="card.title">
          <img class="how__card-icon" :src="card.img" :alt="card.title" @error="e => e.target.style.display='none'" />
          <div class="how__card-body">
            <p class="how__card-title">{{ card.title }}</p>
            <p class="how__card-text">{{ card.text }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="faq">
      <div class="faq__inner">
        <div class="faq__left">
          <h2 class="faq__title">Ответы на вопросы по сервису чат ботов Botolabr</h2>
        </div>
        <div class="faq__right">
          <div class="faq__item" v-for="(item, i) in faqItems" :key="i" :class="{ 'faq__item--open': openFaq === i }">
            <div class="faq__question" @click="toggleFaq(i)">
              <span class="faq__circle"></span>
              <span>{{ item.q }}</span>
              <span class="faq__arrow" :class="{ 'faq__arrow--open': openFaq === i }">&#9660;</span>
            </div>
            <transition name="faq-slide">
              <div class="faq__answer" v-if="openFaq === i">{{ item.a }}</div>
            </transition>
            <div class="faq__divider"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <div class="footer__cols">
        <div class="footer__col footer__col--brand">
          <a class="footer__logo" @click.prevent="scrollToTop">
            <img class="footer__logo-icon" src="/icons.svg" alt="Botolabr" @error="e => e.target.style.display='none'" />
            <span class="footer__logo-text">BOTOLABR</span>
          </a>
          <p class="footer__tagline">Конструктор Telegram-ботов<br/>без единой строки кода</p>
        </div>
      </div>
    </footer>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const menuOpen = ref(false)

function goToLogin(mode = 'login') {
  menuOpen.value = false
  router.push({ path: '/login', query: { mode } })
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ── FAQ аккордеон
const openFaq = ref(null)
function toggleFaq(i) {
  openFaq.value = openFaq.value === i ? null : i
}

// ── Variant tabs
const activeVariant = ref('service')
const variantTabs = [
  { id: 'service', label: 'Сфера услуг',     icon: '/image/service.svg' },
  { id: 'info',    label: 'Инфобизнес',       icon: '/image/infobiznes.svg' },
  { id: 'sale',    label: 'Продажи',          icon: '/image/prodazhi.svg' },
  { id: 'social',  label: 'Введение соц.сетей', icon: '/image/messenger.svg' },
]
const variantContents = {
  service: {
    text1: 'Конструктор роботов востребован в области сервисов. Формирование и конфигурирование чат-ботов через эту систему это оперативное и рациональное подход для предприятия, ориентированного на сбыт услуг или продукции, без лишних расходов и значительных временных затрат.',
    text2: 'Нет необходимости привлекать специалистов для написания программного кода или обработки клиентских запросов. Сформированный чат-бот способен автономно вести диалог с потребителями, привлекать внимание публики.',
    image: '/image/variant1.png',
  },
  info: {
    text1: 'Платформа идеально подходит для создания чат-ботов в сфере информационного бизнеса. Автоматизируйте процесс продажи курсов, вебинаров и электронных продуктов.',
    text2: 'Предоставляйте своим клиентам круглосуточную поддержку и персональные рекомендации на основе их интересов.',
    image: '/image/info.png',
  },
  sale: {
    text1: 'Увеличьте объём продаж с помощью умного чат-бота. Автоматическое квалифицирование лидов, рекомендации товаров и оформление заказов прямо в чате.',
    text2: 'Интегрируйте свой каталог товаров, управляйте скидками и проводите целевые маркетинговые кампании через мессенджеры.',
    image: '/image/sale.png',
  },
  social: {
    text1: 'Расширьте присутствие вашего бренда в социальных сетях. Создавайте чат-ботов для Telegram.',
    text2: 'Управляйте всеми каналами коммуникации из одного интерфейса и собирайте аналитику по взаимодействию с аудиторией.',
    image: '/image/social.png',
  },
}

// ── Текущий контент варианта (computed)
const currentVariant = computed(() => variantContents[activeVariant.value])

// ── Vozmozhnost tabs
const activeVoz = ref('analitics')
const vozmozhnostTabs = [
  { id: 'analitics',   label: 'Аналитика',      icon: '/image/service.svg' },
  { id: 'konstructor', label: 'Конструктор',     icon: '/image/infobiznes.svg' },
  { id: 'dialog',      label: 'Диалоги',         icon: '/image/prodazhi.svg' },
  { id: 'shablony',    label: 'Готовые решения', icon: '/image/messenger.svg' },
]
const vozContents = {
  analitics: {
    image: '/image/variant1.png',
    desc: 'Соберите собственную аудиторию последователей и организуйте периодические оповещения для укрепления доверия и роста объемов реализации.',
    text: 'Отслеживайте ключевые метрики взаимодействия с ботом в режиме реального времени. Принимайте решения на основе данных.',
    list: [
      'Статистика открытий и кликов по каждому сообщению',
      'Воронка конверсии от первого касания до покупки',
      'Сегментация аудитории по поведению и интересам',
      'Выгрузка отчётов в удобном формате',
    ],
  },
  konstructor: {
    image: '/image/info.png',
    desc: 'Создавайте чат-ботов без единой строки кода.',
    text: 'Создавайте чат-ботов визуально — без написания кода. Простой drag-and-drop интерфейс для любого уровня подготовки.',
    list: [
      'Визуальный редактор сценариев и диалогов',
      'Готовые блоки: кнопки, опросы, медиа, оплата',
      'Мгновенный предпросмотр бота прямо в редакторе',
      'Подключение к внешним сервисам через вебхуки',
    ],
  },
  dialog: {
    image: '/image/prodazhi.svg',
    desc: 'Выстраивайте естественные диалоги с пользователями.',
    text: 'Бот ведёт клиента по нужному сценарию автоматически.',
    list: [
      'Ветвистые сценарии с условной логикой',
      'Персонализация ответов на основе данных пользователя',
      'Передача диалога живому оператору при необходимости',
      'История переписки и теги для каждого контакта',
    ],
  },
  shablony: {
    image: '/image/sale.png',
    desc: 'Запустите бота за минуты с помощью проверенных шаблонов.',
    text: 'Просто выберите подходящий и настройте под себя.',
    list: [
      'Шаблоны для интернет-магазинов, услуг и инфобизнеса',
      'Готовые воронки продаж и онбординга',
      'Быстрая настройка без технических знаний',
      'Регулярное пополнение библиотеки новыми шаблонами',
    ],
  },
}

// ── Текущий контент возможности (computed)
const currentVoz = computed(() => vozContents[activeVoz.value])

// ── How cards
const howCards = [
  { img: '/image/img1.png', title: 'Продает за вас',                   text: 'Чат-бот от Botolabr выявит потребности клиента, прогреет их, отсеет ненужных и передаст готовых к покупке людей продавцу.' },
  { img: '/image/img2.png', title: 'Принимает оплату',                 text: 'Его можно использовать для отображения образца шрифтов, создания текста для тестирования.' },
  { img: '/image/img3.png', title: 'Выдает доступ к курсам',           text: 'Если вы продаете курсы, бот примет оплату, получит заказ и выдаст доступ к курсу или тренингу без вашего участия.' },
  { img: '/image/img4.png', title: 'Автоматически рассылает информацию', text: 'Бот вышлет нужную информацию в заданное время заданной категории подписчиков. Не нужно делать это самостоятельно.' },
]

// ── FAQ
const faqItems = [
  {
    q: 'У вас конструктор, платформа или сервис по созданию чат ботов?',
    a: 'Конструктор чат-ботов, платформа и сервис — это все синонимы площадки, где вы делаете собственных чат-ботов. Вы заходите на сайт, регистрируетесь и создаёте виртуального помощника. Сайт является одновременно конструктором и платформой для вас.',
  },
  {
    q: 'У вас можно сделать чат бота онлайн?',
    a: 'Конечно, Botolabr предоставляет услуги онлайн для всех пользователей бесплатно. В начале вы заходите в @Botfather для создания уникального идентификатора. Затем входите в сервис Botolabr и создаёте, настраиваете своего бота.',
  },
  {
    q: 'У вас есть приложение для создания чат ботов и автоворонок?',
    a: 'У конструктора Botolabr нет приложения на мобильные телефоны. Существует только мобильная версия сайта. Это сделано для удобства, а вообще лучше создавать чат-бота через браузер на компьютере или ноутбуке.',
  },
  {
    q: 'Как долго можно пользоваться бесплатным тарифом?',
    a: 'Бесплатный тариф доступен без ограничений по времени. Вы можете пользоваться им столько, сколько вам нужно. При необходимости расширить возможности — просто перейдите на один из платных тарифов в любой момент.',
  },
]
</script>

<style scoped>
/* =============================================
   RESET
============================================= */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

.landing {
  background: #F6FEDE;
  font-family: "Roboto-slab", sans-serif;
  color: #1f3f16;
  overflow-x: hidden;
}

/* =============================================
   HEADER
============================================= */
.header {
  width: 100%;
  padding: 10px 0;
  background: #F6FEDE;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 1px 0 rgba(11,80,0,0.08);
}

.header__row {
  width: 100%;
  padding: 0 80px;
  display: flex;
  align-items: center;
  gap: 100px;
}

.logo {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo img {
  height: 50px;
  width: auto;
  transition: transform 0.3s ease;
}
.logo img:hover { transform: scale(1.05); }

.logo__fallback {
  font-weight: 700;
  font-family: 'Lobelia', serif;
  font-size: 18px;
  color: #0B5000;
  letter-spacing: 0.05em;
}

.header__buttons {
  display: flex;
  gap: 24px;
  flex-shrink: 0;
  margin-left: auto;
  align-items: center;
}

/* Бургер — скрыт на десктопе */
.burger {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 36px;
  height: 36px;
  background: none;
  border: none;
  cursor: pointer;
  margin-left: auto;
  padding: 4px;
  flex-shrink: 0;
}
.burger span {
  display: block;
  width: 100%;
  height: 3px;
  background: #0B5000;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}
.burger.open span:nth-child(1) { transform: translateY(8px) rotate(45deg); }
.burger.open span:nth-child(2) { opacity: 0; }
.burger.open span:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }

/* =============================================
   BUTTONS
============================================= */
.btn {
  border: none;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-family: 'Roboto Slab', serif;
  font-weight: bold;
  font-size: 18px;
  color: #F6FEDE;
  white-space: nowrap;
}

.btn--outline {
  width: 90px;
  height: 35px;
  border-radius: 25px;
  background: #0B5000;
  border: 2px solid #0B5000;
}
.btn--outline:hover {
  background: #083d00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(11,80,0,0.3);
}

.btn--solid {
  width: 140px;
  height: 35px;
  border-radius: 25px;
  background: #0B5000;
  border: 2px solid #0B5000;
}
.btn--solid:hover {
  background: #083d00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(11,80,0,0.3);
}

.btn--variant {
  margin-top: 40px;
  width: 100%;
  max-width: 250px;
  height: 45px;
  border-radius: 30px;
  background: #0B5000;
  border: 2px solid #0B5000;
  font-size: 18px;
  font-family: 'Roboto Slab', serif;
  font-weight: bold;
  color: #F6FEDE;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.3s ease;
}
.btn--variant:hover {
  background: #083d00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(11,80,0,0.3);
}

.btn--vozmozhnost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-top: 40px;
  width: 100%;
  max-width: 250px;
  height: 45px;
  border-radius: 30px;
  background: #0B5000;
  border: 2px solid #0B5000;
  font-size: 18px;
  font-family: 'Roboto Slab', serif;
  font-weight: bold;
  color: #F6FEDE;
  white-space: nowrap;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
}
.btn--vozmozhnost:hover {
  background: #083d00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(11,80,0,0.3);
}

.btn--about {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  max-width: 250px;
  height: 45px;
  border-radius: 30px;
  background: #0B5000;
  border: 2px solid #0B5000;
  font-size: 18px;
  font-family: 'Roboto Slab', serif;
  font-weight: bold;
  color: #F6FEDE;
  white-space: nowrap;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.3s ease;
}
.btn--about:hover {
  background: #083d00;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(11,80,0,0.3);
}

/* =============================================
   HERO
============================================= */
.hero {
  width: 100%;
  min-height: 100svh;
  background: #F6FEDE;
  position: relative;
  overflow: hidden;
}

.hero__row {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: inherit;
}

/* Десктоп — абсолютное позиционирование как в оригинале, масштабируется через vw */
.hero__text {
  position: absolute;
  left: clamp(20px, 15vw, 150px);
  top: clamp(90px, 32vw, 200px);
  font-family: 'Lobelia', serif;
  font-weight: 400;
  font-size: clamp(36px, 6vw, 56px);
  color: #0B5000;
  text-shadow: 14px 8px 10px #CDFF9E;
  line-height: 75%;
  letter-spacing: 1px;
}

.hero__konstruktor {
  position: absolute;
  left: clamp(20px, 25vw, 240px);
  top: clamp(180px, 48vw, 400px);
  font-family: 'NauryzRedKeds', serif;
  font-weight: bold;
  font-size: clamp(24px, 8vw, 64px);
  color: #0B5000;
  white-space: nowrap;
  line-height: 75%;
  letter-spacing: 1px;
}

.hero__dlya {
  position: absolute;
  left: clamp(150px, 68vw, 700px);
  top: clamp(260px, 45vw, 375px);
  font-family: 'Gogol', serif;
  font-weight: 400;
  font-size: clamp(20px, 6vw, 40px);
  color: #ADF36C;
  white-space: nowrap;
  text-decoration: underline;
  text-decoration-style: dashed;
  text-decoration-color: #0B5000;
  text-underline-offset: 12px;
  text-decoration-thickness: 3px;
  line-height: 75%;
  letter-spacing: 1px;
}

.hero__chatbotov {
  position: absolute;
  left: clamp(200px, 70vw, 700px);
  top: clamp(320px, 53vw, 425px);
  font-family: 'NauryzRedKeds', serif;
  font-weight: bold;
  font-size: clamp(22px, 6vw, 56px);
  color: #0B5000;
  white-space: nowrap;
  line-height: 75%;
  letter-spacing: 1px;
}

.hero__image {
  position: absolute;
  right: clamp(80px, 15vw, 180px);
  top: clamp(20px, 10vw, 40px);
  width: clamp(200px, 45vw, 650px);
  height: auto;
  pointer-events: none;
}
.hero__image img {
  width: 100%;
  height: auto;
  display: block;
}

/* =============================================
   VARIANT
============================================= */
.variant {
  width: 100%;
  background: #ADF36C;
  padding-bottom: 60px;
}

.variant__header {
  padding: 75px 5% 30px 5%;
}

.variant__text h1 {
  font-family: 'NauryzRedKeds', serif;
  font-weight: 400;
  font-size: clamp(22px, 4.5vw, 36px);
  color: #0B5000;
  text-shadow: 12px 8px 10px rgba(31,63,22,0.3);
  margin-bottom: 32px;
  line-height: 75%;
  letter-spacing: 1px;
}

.variant__description {
  font-family: 'Roboto Slab', serif;
  font-weight: 400;
  font-size: clamp(14px, 2vw, 18px);
  color: #000000;
  line-height: 1.6;
  letter-spacing: 1px;
}

.variant__tabs {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  padding: 0 5%;
  position: relative;
  border-bottom: 3px solid rgba(11,80,0,0.3);
}

.tab {
  padding: 12px 0;
  background: transparent;
  color: #000000;
  border: none;
  border-radius: 0;
  cursor: pointer;
  font-family: inherit;
  font-weight: 500;
  font-size: clamp(16px, 2vw, 20px);
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  margin-bottom: -3px;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 10px;
}
.tab__icon { width: 24px; height: 24px; transition: transform 0.3s ease; flex-shrink: 0; }
.tab:hover { color: #0B5000; transform: translateY(-2px); }
.tab:hover .tab__icon { transform: scale(1.15); }
.tab.active { color: #000000; border-bottom-color: #000000; }
.tab.active .tab__icon { transform: scale(1.1); }

.variant__contents {
  padding: 40px 5%;
  min-height: 300px;
}

.variant__content-wrapper {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.variant__content-text { flex: 1; }

.variant__content p {
  margin: 0 0 16px 0;
  font-size: clamp(14px, 2vw, 18px);
  font-family: 'Roboto Slab', serif;
  font-weight: 500;
  line-height: 1.6;
  letter-spacing: 1px;
  color: #000000;
}

.variant__content-image {
  width: clamp(200px, 30vw, 500px);
  height: clamp(150px, 22vw, 380px);
  background: #F6FEDE;
  background-size: cover;
  background-position: center;
  border-radius: 40px;
  flex-shrink: 0;
  border: 3px dashed rgba(11, 80, 0, 0.7);
}

/* =============================================
   VOZMOZHNOST
============================================= */
.vozmozhnost {
  width: 100%;
  background: #F6FEDE;
  padding-bottom: 60px;
}

.vozmozhnost__header {
  padding: 75px 5% 30px 5%;
}

.vozmozhnost__text h1 {
  font-family: 'NauryzRedKeds', serif;
  font-weight: 400;
  font-size: clamp(22px, 4.5vw, 36px);
  color: #0B5000;
  text-shadow: 12px 8px 10px rgba(31,63,22,0.3);
  margin-bottom: 16px;
  line-height: 75%;
  letter-spacing: 1px;
}

.vozmozhnost__tabs {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  padding: 0 5%;
  position: relative;
  border-bottom: 3px solid rgba(11,80,0,0.3);
}

.tab1 {
  padding: 12px 0;
  background: transparent;
  color: #000000;
  border: none;
  border-radius: 0;
  cursor: pointer;
  font-family: inherit;
  font-weight: 500;
  font-size: clamp(16px, 2vw, 20px);
  transition: all 0.3s ease;
  border-bottom: 3px solid transparent;
  margin-bottom: -3px;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 10px;
}
.tab1__icon { width: 24px; height: 24px; transition: transform 0.3s ease; flex-shrink: 0; }
.tab1:hover { color: #0B5000; transform: translateY(-2px); }
.tab1:hover .tab1__icon { transform: scale(1.15); }
.tab1.active { color: #000000; border-bottom-color: #0B5000; }
.tab1.active .tab1__icon { transform: scale(1.1); }

.vozmozhnost__contents {
  padding: 40px 5%;
  min-height: 300px;
}

.vozmozhnost__content-wrapper {
  display: flex;
  gap: 40px;
  align-items: flex-start;
}

.vozmozhnost__content-image {
  width: clamp(200px, 30vw, 500px);
  height: clamp(150px, 22vw, 380px);
  background: #ADF36C;
  background-size: cover;
  background-position: center;
  border-radius: 40px;
  flex-shrink: 0;
  border: 3px dashed rgba(11, 80, 0, 0.7);

}

.vozmozhnost__content-right {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.vozmozhnost__description {
  font-family: 'Roboto Slab', serif;
  font-weight: 400;
  font-size: clamp(14px, 2vw, 18px);
  color: #000000;
  line-height: 1.6;
  letter-spacing: 1px;
}

.vozmozhnost__content-text p {
  font-size: clamp(14px, 2vw, 18px);
  font-family: 'Roboto Slab', serif;
  font-weight: 400;
  line-height: 1.6;
  letter-spacing: 1px;
  color: #000000;

}

.vozmozhnost__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.vozmozhnost__list li {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-family: 'Roboto Slab', serif;
  font-size: clamp(14px, 2vw, 18px);
  font-weight: 400;
  color: #000;
  line-height: 1.6;
  letter-spacing: 1px;
}
.vozmozhnost__list li::before {
  content: '';
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  min-width: 18px;
  background: #0B5000;
  border-radius: 50%;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'/%3E%3C/svg%3E");
  background-size: 45%;
  background-repeat: no-repeat;
  background-position: center;
  margin-top: 4px;
  flex-shrink: 0;
}

/* =============================================
   ABOUT
============================================= */
.about {
  width: 100%;
  background-color: #ADF36C;
  position: relative;
  overflow: hidden;
}
.about::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/image/frame1.png') no-repeat center center / cover;
  opacity: 0.2;
  z-index: 0;
}
.about__inner {
  position: relative;
  z-index: 1;
  padding: 60px 5%;
}

.about__title {
  font-family: 'NauryzRedKeds', serif;
  font-weight: 400;
  font-size: clamp(22px, 4vw, 36px);
  color: #0B5000;
  text-shadow: 10px 6px 8px rgba(31,63,22,0.3);
  margin: 40px 0 40px 0;
  line-height: 1;
  letter-spacing: 1px;
}
.about__text {
  font-family: 'NauryzRedKeds', serif;
  font-weight: 400;
  font-size: clamp(16px, 3vw, 28px);
  color: #000000;
  line-height: 2;
  margin: 0 0 24px 0;
  letter-spacing: 1px;
}

/* =============================================
   HOW
============================================= */
.how {
  width: 100%;
  background: #F6FEDE;
  padding: 60px 5%;
}

.how__title {
  font-family: 'NauryzRedKeds', serif;
  font-weight: 400;
  font-size: clamp(22px, 4vw, 36px);
  color: #0B5000;
  text-align: center;
  line-height: 1.6;
  margin-bottom: 50px;
  text-shadow: 8px 6px 8px rgba(31,63,22,0.2);
  letter-spacing: 1px;
}
.how__title span {
  color: #ADF36C;
  border-bottom: 3px dashed #0B5000;
  padding-bottom: 4px;
  letter-spacing: 1px;
}

.how__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px 60px;
}

.how__card {
  display: flex;
  align-items: flex-start;
  gap: 20px;
}

.how__card-icon {
  width: clamp(40px, 12vw, 90px);
  height: clamp(40px, 12vw, 90px);
  min-width: clamp(40px, 12vw, 90px);
  object-fit: contain;
  display: block;
}

.how__card-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding-top: 16px;
}

.how__card-title {
  font-family: 'Roboto Slab', serif;
  font-weight: 700;
  font-size: clamp(16px, 1.8vw, 20px);
  color: #0B5000;
  letter-spacing: 1px;
}
.how__card-text {
  font-family: 'Roboto Slab', serif;
  font-weight: 400;
  font-size: clamp(14px, 1.6vw, 18px);
  color: #000000;
  line-height: 1.6;
  letter-spacing: 1px;
}

/* =============================================
   FAQ
============================================= */
.faq {
  width: 100%;
  background: #0B5000;
  padding: 60px 0;
}
.faq__inner {
  width: 100%;
  padding: 0 5%;
  display: flex;
  gap: 60px;
  align-items: flex-start;
}
.faq__left {
  width: clamp(200px, 30vw, 520px);
  min-width: clamp(200px, 30vw, 520px);
  flex-shrink: 0;
}
.faq__title {
  font-family: 'Lobelia', serif;
  font-weight: 400;
  font-size: clamp(22px, 4vw, 36px);
  line-height: 1.6;
  letter-spacing: 1px;
  color: #ADF36C;
  text-transform: uppercase;
}
.faq__right {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.faq__item {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 24px 0 0 0;
}
.faq__question {
  display: flex;
  align-items: center;
  gap: 12px;
  font-family: 'Roboto Slab', serif;
  font-weight: 700;
  font-size: clamp(16px, 1.6vw, 20px);
  color: #ADF36C;
  line-height: 1.6;
  letter-spacing: 1px;
  cursor: pointer;
  user-select: none;
  transition: opacity 0.2s;
}
.faq__question:hover { opacity: 0.8; }
.faq__arrow {
  margin-left: auto;
  font-size: clamp(12px, 2vw, 14px);
  color: #ADF36C;
  transition: transform 0.3s ease;
  flex-shrink: 0;
  line-height: 1;
}
.faq__arrow--open { transform: rotate(180deg); }
.faq__item--open .faq__circle {
  background: #ADF36C;
}
.faq__circle {
  display: inline-block;
  width: 14px;
  height: 14px;
  min-width: 14px;
  border-radius: 50%;
  border: 2px solid #ADF36C;
  margin-top: 3px;
  flex-shrink: 0;
}
.faq__answer {
  font-family: 'Roboto Slab', serif;
  font-weight: 400;
  font-size: clamp(14px, 2vw, 18px);
  color: #ADF36C;
  line-height: 1.6;
  letter-spacing: 1px;
  padding-left: 30px;
  margin-bottom: 12px;
}
.faq__divider {
  width: 100%;
  height: 1px;
  background: rgba(173,243,108,0.3);
}

/* =============================================
   FOOTER
============================================= */
.footer {
  width: 100%;
  background: #F6FEDE;
  padding: 0;
}

/* Колонки */
.footer__cols {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: 40px;
  padding: 48px 5% 40px;
}
.footer__col--brand { padding-right: 20px; }

.footer__logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  gap: 12px;
  cursor: pointer;
  margin-bottom: 16px;
}
.footer__logo-icon { width: 48px; height: 48px; object-fit: contain; }
.footer__logo-text {
  font-family: 'Lobelia', serif;
  font-weight: 400;
  font-size: clamp(20px, 2vw, 28px);
  color: #0B5000;
  letter-spacing: 0.05em;
}
.footer__tagline {
  font-family: 'Roboto Slab', serif;
  font-size: clamp(12px, 1.2vw, 15px);
  color: #0B5000;
  line-height: 1.7;
  margin-bottom: 24px;
}

/* =============================================
   TRANSITION
============================================= */
.tab-fade-enter-active, .tab-fade-leave-active {
  transition: opacity 0.25s ease;
}
.tab-fade-enter-from, .tab-fade-leave-to { opacity: 0; }
.tab-fade-enter-to, .tab-fade-leave-from { opacity: 1; }

/* скрыть перенос строки на мобиле */
.br-desktop { display: block; }

/* =============================================
   FAQ SLIDE TRANSITION
============================================= */
.faq-slide-enter-active {
  transition: all 0.3s ease;
  overflow: hidden;
}
.faq-slide-leave-active {
  transition: all 0.25s ease;
  overflow: hidden;
}
.faq-slide-enter-from,
.faq-slide-leave-to {
  max-height: 0;
  opacity: 0;
  margin-top: 0;
  margin-bottom: 0;
}
.faq-slide-enter-to,
.faq-slide-leave-from {
  max-height: 400px;
  opacity: 1;
}

/* =============================================
   RESPONSIVE — TABLET (max 1024px)
============================================= */
@media (max-width: 1024px) {
  .header__row { padding: 0 32px; gap: 40px; }

  .hero__text    { left: 5%; top: 25vw; }
  .hero__konstruktor { left: 10%; top: 40vw; }
  .hero__dlya    { left: 58%; top: 37vw; }
  .hero__chatbotov { left: 58%; top: 47vw; }
  .hero__image   { width: 38vw; right: 0; top: 10vw; }

  .variant__content-image {
    width: clamp(160px, 25vw, 340px);
    height: clamp(120px, 18vw, 280px);
  }
  .vozmozhnost__content-image {
    width: clamp(160px, 25vw, 340px);
    min-width: clamp(160px, 25vw, 340px);
    height: clamp(120px, 18vw, 280px);
  }

  .how__grid { gap: 30px 40px; }
  .faq__left { width: clamp(160px, 25vw, 320px); min-width: clamp(160px, 25vw, 320px); }
}

/* =============================================
   RESPONSIVE — MOBILE (max 768px)
============================================= */
@media (max-width: 768px) {
  /* Header */
  .header__row { padding: 0 20px; gap: 0; }
  .burger { display: flex; }
  .header__buttons {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #f6ffe3;
    flex-direction: column;
    align-items: stretch;
    padding: 16px 20px;
    gap: 12px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    z-index: 200;
    margin-left: 0;
  }
  .header__buttons--open { display: flex; }
  .header__buttons .btn { width: 100%; font-size: 16px; height: 44px; }

  /* Hero — убираем абсолютное позиционирование, делаем обычный поток */
  .hero { min-height: auto; padding: 100px 20px 40px; }
  .hero__row {
    position: static;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    min-height: auto;
  }
  .hero__text, .hero__konstruktor, .hero__dlya, .hero__chatbotov {
    position: static;
    white-space: normal;
  }
  .hero__text    { font-size: clamp(36px, 10vw, 64px); margin-bottom: 4px; }
  .hero__konstruktor { font-size: clamp(28px, 9vw, 56px); }
  .hero__dlya    { font-size: clamp(22px, 7vw, 44px); align-self: flex-end; }
  .hero__chatbotov   { font-size: clamp(22px, 7vw, 44px); }
  .hero__image { position: static; width: 70%; align-self: center; margin-top: 24px; }

  /* Variant */
  .variant__content-wrapper { flex-direction: column; }
  .variant__content-image {
    width: 100%;
    height: 180px;
    border-radius: 20px;
  }
  .variant__tabs { gap: 12px; padding: 0 20px; }
  .tab { font-size: 14px; gap: 6px; }
  .tab__icon { width: 18px; height: 18px; }
  .variant__header { padding: 32px 20px 20px; }
  .variant__contents { padding: 24px 20px; }

  /* Vozmozhnost */
  .vozmozhnost__content-wrapper { flex-direction: column; }
  .vozmozhnost__content-image {
    width: 100%;
    min-width: unset;
    height: 180px;
    border-radius: 20px;
  }
  .vozmozhnost__tabs { gap: 12px; padding: 0 20px; }
  .tab1 { font-size: 14px; gap: 6px; }
  .tab1__icon { width: 18px; height: 18px; }
  .vozmozhnost__header { padding: 16px 20px 0; }
  .vozmozhnost__contents { padding: 24px 20px; }
  .vozmozhnost__text h1 { margin: 20px 0 16px; }
  .btn--vozmozhnost { max-width: 100%; }

  /* About */
  .about__inner { padding: 40px 20px; }
  .about__title { margin: 16px 0 24px; }
  .about__text { line-height: 1.6; margin-bottom: 16px; }
  .btn--about { max-width: 100%; }

  /* How */
  .how { padding: 40px 20px; }
  .how__grid { grid-template-columns: 1fr; gap: 28px; }
  .how__card-icon {
    width: 70px; height: 70px; min-width: 70px;
  }

  /* FAQ */
  .faq__inner { flex-direction: column; padding: 0 20px; gap: 32px; }
  .faq__left { width: 100%; min-width: unset; }

  /* Footer */
  .footer__top { flex-direction: column; align-items: flex-start; gap: 20px; padding: 32px 20px; }
  .footer__top-actions { width: 100%; }
  .footer__btn-register, .footer__btn-login { flex: 1; text-align: center; }
  .footer__cols { grid-template-columns: 1fr 1fr; gap: 28px; padding: 32px 20px 28px; }
  .footer__col--brand { grid-column: 1 / -1; padding-right: 0; }
  .footer__bottom { padding: 16px 20px; flex-direction: column; align-items: flex-start; gap: 4px; }
  .footer__divider-line { margin: 0 20px; }

  .br-desktop { display: none; }
}

/* =============================================
   RESPONSIVE — SMALL MOBILE (max 480px)
============================================= */
@media (max-width: 480px) {
  .hero__konstruktor { font-size: 9vw; }
  .variant__tabs, .vozmozhnost__tabs { gap: 8px; }
  .tab, .tab1 { font-size: 13px; padding: 8px 0; }
  .faq__title { font-size: 22px; }
  .footer__cols { grid-template-columns: 1fr; }
  .footer__col--brand { grid-column: auto; }
  .footer__top-actions { flex-direction: column; }
  .footer__btn-register, .footer__btn-login { width: 100%; }
}
</style>
