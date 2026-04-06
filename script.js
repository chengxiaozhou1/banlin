// ===== 导航栏滚动效果 =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 50);
});

// ===== 移动端菜单 =====
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const navLinks = document.getElementById('navLinks');

mobileMenuBtn.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    mobileMenuBtn.classList.toggle('active');
});

// 点击导航链接后关闭菜单
navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        mobileMenuBtn.classList.remove('active');
    });
});

// ===== 数字动画 =====
function animateCounters() {
    const counters = document.querySelectorAll('.stat-num[data-target]');
    counters.forEach(counter => {
        const target = parseInt(counter.dataset.target);
        const duration = 2000;
        const start = performance.now();

        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            // easeOutExpo
            const eased = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
            counter.textContent = Math.floor(target * eased).toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        requestAnimationFrame(update);
    });
}

// 用 IntersectionObserver 触发数字动画
const statsSection = document.querySelector('.hero-stats');
if (statsSection) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    observer.observe(statsSection);
}

// ===== 滚动渐入动画 =====
const fadeElements = document.querySelectorAll(
    '.about-card, .step-card, .service-card, .story-card, .trust-item, .pain-item, .benefit-item, .pricing-card, .companion-profile'
);

fadeElements.forEach(el => el.classList.add('fade-in'));

const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            // 给每个元素添加延迟，产生依次出现的效果
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, index * 80);
            fadeObserver.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

fadeElements.forEach(el => fadeObserver.observe(el));

// ===== 表单提交 =====
const bookingForm = document.getElementById('bookingForm');
const applyForm = document.getElementById('applyForm');
const successModal = document.getElementById('successModal');

// 自动检测：本地开发用 localhost，线上用当前域名
const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:5001/api'
    : window.location.origin + '/api';

if (bookingForm) {
    bookingForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 收集表单数据
        const services = [];
        bookingForm.querySelectorAll('input[name="services"]:checked').forEach(cb => {
            services.push(cb.value);
        });

        const payload = {
            name: bookingForm.querySelector('input[name="name"]').value,
            phone: bookingForm.querySelector('input[name="phone"]').value,
            email: bookingForm.querySelector('input[name="email"]').value,
            relationship: bookingForm.querySelector('select[name="relationship"]').value,
            age: bookingForm.querySelector('input[name="age"]').value,
            district: bookingForm.querySelector('select[name="district"]').value,
            services: services,
            remarks: bookingForm.querySelector('textarea[name="remarks"]').value
        };

        try {
            const response = await fetch(`${API_BASE_URL}/booking`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (result.success) {
                successModal.classList.add('active');
                bookingForm.reset();
            } else {
                alert('提交失败：' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('提交失败，请检查网络连接');
        }
    });
}

if (applyForm) {
    applyForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // 收集表单数据
        const availableTime = [];
        applyForm.querySelectorAll('input[name="availableTime"]:checked').forEach(cb => {
            availableTime.push(cb.value);
        });

        const payload = {
            name: applyForm.querySelector('input[name="name"]').value,
            phone: applyForm.querySelector('input[name="phone"]').value,
            email: applyForm.querySelector('input[name="email"]').value,
            age: applyForm.querySelector('input[name="age"]').value,
            identity: applyForm.querySelector('select[name="identity"]').value,
            district: applyForm.querySelector('select[name="district"]').value,
            availableTime: availableTime,
            motivation: applyForm.querySelector('textarea[name="motivation"]').value
        };

        try {
            const response = await fetch(`${API_BASE_URL}/apply`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();

            if (result.success) {
                document.getElementById('applyModal').classList.remove('active');
                successModal.classList.add('active');
                applyForm.reset();
            } else {
                alert('提交失败：' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('提交失败，请检查网络连接');
        }
    });
}

// 点击遮罩层关闭弹窗
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            overlay.classList.remove('active');
        }
    });
});

// ESC 关闭弹窗
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(m => {
            m.classList.remove('active');
        });
    }
});

// ===== 平滑滚动 =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        const targetEl = document.querySelector(targetId);
        if (targetEl) {
            e.preventDefault();
            const navHeight = navbar.offsetHeight;
            const targetPos = targetEl.getBoundingClientRect().top + window.scrollY - navHeight - 20;
            window.scrollTo({
                top: targetPos,
                behavior: 'smooth'
            });
        }
    });
});
