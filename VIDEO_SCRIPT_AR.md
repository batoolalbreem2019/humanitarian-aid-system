# سكريبت الفيديو — Running Project النهائي
## Humanitarian Aid Management System
**الطالبة:** بتول البريم | 220197079 | د. عبد الكريم الأشقر | SDEV 4304

---

## 🎬 الجزء الأول — المقدمة (1 دقيقة | 0:00–1:00)

السلام عليكم ورحمة الله وبركاته،
اسمي **بتول البريم**، رقمي الجامعي **220197079**.
المادة: **Advanced Software Engineering — SDEV 4304**.
الدكتور المشرف: **الدكتور عبد الكريم الأشقر**.
الجامعة الإسلامية بغزة | الفصل الثاني 2025/2026.

في هذا الفيديو سأعرض مشروعي النهائي: **Humanitarian Aid Management System** —
منصة رقمية لإدارة وتوزيع المساعدات الإنسانية، مبنية على معمارية الـ Microservices باستخدام Django وDocker.

---

## 📄 الجزء الثاني — الوثيقة (7 دقائق | 1:00–8:00)

### وصف النظام (1:00–2:00)
المشروع عبارة عن منصة رقمية تتيح للمنظمات تسجيل المستفيدين وتتبع احتياجاتهم وإدارة توزيع الموارد كالغذاء والدواء والدعم المالي.
المتطوعون ينسقون عمليات التوصيل، والمانحون يتابعون استخدام تبرعاتهم.
النظام يعزز الشفافية ويضمن وصول المساعدات للمستحقين بسرعة وكفاءة.

### المعمارية (2:00–4:00)
النظام مبني على معمارية الـ Microservices كما يصفها Sam Newman في كتابه Building Microservices.
يتكون من **5 خدمات مستقلة**:
- **User Service** (8001) — إدارة الهويات والمصادقة
- **Aid Request Service** (8002) — تقديم وتتبع طلبات المساعدة
- **Donation Service** (8003) — إدارة التبرعات
- **Distribution Service** (8004) — جدولة وتتبع التوصيل
- **Notification Service** (8005) — إرسال الإشعارات

كل خدمة لها قاعدة بيانات PostgreSQL مستقلة — لا مشاركة في البيانات.

### أسلوب التواصل (4:00–5:30)
الخدمات تتواصل بأسلوبين (Newman Ch.4):
- **Synchronous REST** في حالتين فقط حيث الاستجابة ضرورية لاستكمال العملية
- **Async Event-Driven** عبر RabbitMQ في بقية الحالات — Fat events تحمل كل البيانات

### Saga Pattern (5:30–6:30)
عملية الموافقة على الطلب تُطبّق كـ Saga (Newman Ch.6):
T1: Aid Request → T2: Donation → T3: Distribution → T4: Notification
عند فشل T3، تعمل Compensating Transactions بترتيب عكسي: C2 تُلغي الحجز، C1 تُلغي الطلب.

### Build & Deployment (6:30–8:00)
- **Monorepo** على GitHub — كل خدمة لها build مستقل
- **CI/CD** بـ GitHub Actions — pipeline منفصل لكل خدمة
- **Docker** — كل خدمة packaged كـ Docker image تشغّل Gunicorn

---

## 💻 الجزء الثالث — التطبيق بـ Django (5 دقائق | 8:00–13:00)

### 8:00–9:00 — هيكل الكود
افتح VS Code واعرضي هيكل المشروع:
```
humanitarian-aid-system/
├── user_service/
├── aid_request_service/
├── donation_service/
├── distribution_service/
├── notification_service/
└── docker-compose.yml
```

### 9:00–10:30 — User Service
افتحي user_service/users/models.py — اشرحي الـ User model بحقوله الـ 8
افتحي views.py — اشرحي UserRegisterView و UserDetailView
افتحي urls.py — اشرحي الـ 3 endpoints

### 10:30–12:00 — Aid Request Service
افتحي aid_requests/models.py — اشرحي AidRequest والـ status choices
افتحي events.py — اشرحي publish_event() وكيف ترسل Fat event لـ RabbitMQ
افتحي views.py — اشرحي perform_create() الذي ينشر الحدث بعد الحفظ

### 12:00–13:00 — Notification Consumer
افتحي notifications/consumer.py — اشرحي callback() وكيف يستجيب لكل نوع حدث

---

## 🐳 الجزء الرابع — Docker Desktop (5 دقائق | 13:00–18:00)

### 13:00–14:00 — Dockerfile
افتحي user_service/Dockerfile واشرحي كل سطر:
- FROM python:3.12-slim
- pip install requirements
- CMD gunicorn

### 14:00–15:30 — docker-compose.yml
افتحي docker-compose.yml واشرحي:
- 5 service containers + 5 DB containers + RabbitMQ
- كل service له environment variables منفصلة
- depends_on يضمن الترتيب الصحيح

### 15:30–17:30 — تشغيل المشروع
افتحي Terminal وشغّلي:
```bash
docker compose up --build
```
اعرضي Docker Desktop وكل الـ containers شغّالة (11 container)

### 17:30–18:00 — اختبار API
افتحي Postman:
POST localhost:8001/api/users/register/ → اعرضي 201 Created
POST localhost:8002/api/aid-requests/ → اعرضي 201 Created + requestId

---

## ⚙️ الجزء الخامس — CI/CD (3 دقائق | 18:00–21:00)

افتحي .github/workflows/user_service_ci.yml واشرحي:
- paths: filter — يشتغل فقط لما يتغير user_service
- المراحل: flake8 → pytest → docker build → docker push
افتحي GitHub Actions tab واعرضي pipeline run ناجح
افتحي Docker Hub واعرضي الـ image المرفوعة

---

## 🎓 الجزء السادس — ما تعلّمته (4 دقائق | 21:00–25:00)

### المعرفة النظرية:
من خلال هذه المادة تعلّمت:
- تصميم أنظمة على معمارية الـ Microservices (bounded contexts, aggregates)
- أنواع التواصل بين الخدمات: Sync vs Async، Fat events، Temporal coupling
- Saga pattern وCompensating transactions لإدارة العمليات الموزعة
- CI/CD pipelines: build once deploy everywhere
- Docker وcontainerisation وKubernetes concepts

### المهارات العملية:
- بناء REST APIs بـ Django REST Framework من الصفر
- تطبيق event-driven architecture بـ RabbitMQ
- كتابة Dockerfiles وdocker-compose.yml
- إعداد GitHub Actions pipelines

### تأثير هذه المهارات مستقبلاً:
هذه المهارات تُؤهّلني لـ:
- العمل في شركات تبني أنظمة كبيرة على microservices
- تولّي أدوار Backend Developer أو DevOps Engineer
- المشاركة في مشاريع مفتوحة المصدر تستخدم هذه التقنيات
- بناء مشاريع مستقلة قابلة للتوسع من البداية

أهم ما تعلّمته: أن الـ architecture decisions مش مجرد نظرية — كل قرار له مبرر واضح من Newman وله أثر مباشر على قابلية النظام للتوسع والصيانة.

---

## 🎬 الخاتمة (25:00–25:30)

شكراً جزيلاً للاستماع.
أشكر الدكتور عبد الكريم الأشقر على توجيهاته طوال الفصل.
والسلام عليكم ورحمة الله وبركاته.
