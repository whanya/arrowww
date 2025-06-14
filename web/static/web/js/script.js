document.addEventListener("DOMContentLoaded", function() {
   
    const initHorizontalScroll = () => {
      const scroll = document.querySelector(".scroll");
      if (!scroll) return;
  
      let isDown = false;
      let scrollX;
      let scrollLeft;
  
      const handleMouseUp = () => {
        isDown = false;
        scroll.classList.remove("active");
      };
  
      const handleMouseLeave = () => {
        isDown = false;
        scroll.classList.remove("active");
      };
  
      const handleMouseDown = (e) => {
        e.preventDefault();
        isDown = true;
        scroll.classList.add("active");
        scrollX = e.pageX - scroll.offsetLeft;
        scrollLeft = scroll.scrollLeft;
      };
  
      const handleMouseMove = (e) => {
        if (!isDown) return;
        e.preventDefault();
        const element = e.pageX - scroll.offsetLeft;
        const scrolling = (element - scrollX) * 2;
        scroll.scrollLeft = scrollLeft - scrolling;
      };
  
      scroll.addEventListener("mouseup", handleMouseUp);
      scroll.addEventListener("mouseleave", handleMouseLeave);
      scroll.addEventListener("mousedown", handleMouseDown);
      scroll.addEventListener("mousemove", handleMouseMove);
  
      scroll.addEventListener("touchstart", (e) => {
        isDown = true;
        scrollX = e.touches[0].pageX - scroll.offsetLeft;
        scrollLeft = scroll.scrollLeft;
      });
  
      scroll.addEventListener("touchend", handleMouseUp);
      scroll.addEventListener("touchmove", (e) => {
        if (!isDown) return;
        const element = e.touches[0].pageX - scroll.offsetLeft;
        const scrolling = (element - scrollX) * 2;
        scroll.scrollLeft = scrollLeft - scrolling;
      });
    };
  
    const initTabs = () => {
      const openTab = (tabName) => {
        const tabContents = document.querySelectorAll(".tab-content");
        const tabLinks = document.querySelectorAll(".services-button");
        
        // Скрываем все вкладки
        tabContents.forEach(content => {
          content.style.display = "none";
        });
        
        // Удаляем активный класс у всех кнопок
        tabLinks.forEach(link => {
          link.classList.remove("active");
        });
    
        // Показываем выбранную вкладку
        const activeTab = document.getElementById(tabName);
        if (activeTab) {
          activeTab.style.display = "flex";
          activeTab.style.flexDirection = "column";
          activeTab.style.opacity = "0";
          
          // Добавляем плавное появление
          setTimeout(() => {
            activeTab.style.transition = "opacity 0.3s ease";
            activeTab.style.opacity = "1";
          }, 10);
        }
    
        // Добавляем активный класс к выбранной кнопке
        const activeLink = document.getElementById(`${tabName}Link`);
        if (activeLink) {
          activeLink.classList.add("active");
        }
      };
    
      // Вешаем обработчики на все кнопки вкладок
      document.querySelectorAll('[id$="Link"]').forEach(link => {
        link.addEventListener("click", (e) => {
          e.preventDefault();
          const tabName = link.id.replace("Link", "");
          openTab(tabName);
          
          // Прокрутка к началу блока услуг на мобильных
          if (window.innerWidth <= 768) {
            document.getElementById('services').scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          }
        });
      });
    
      // Активируем первую вкладку при загрузке
      const defaultTabLink = document.querySelector('[id$="Link"]');
      if (defaultTabLink) {
        const defaultTabName = defaultTabLink.id.replace("Link", "");
        openTab(defaultTabName);
      }
    };
  
    const initBurgerMenu = () => {
        const burgerButton = document.getElementById('burgerButton');
        const burgerMenu = document.getElementById('burgerMenu');
        const body = document.body;
    
        if (burgerButton && burgerMenu) {
          const overlay = document.createElement('div');
          overlay.className = 'menu-overlay';
          document.body.appendChild(overlay);
    
          const toggleMenu = (e) => {
            if (e) e.preventDefault();
            
            burgerButton.classList.toggle('active');
            burgerMenu.classList.toggle('active');
            overlay.classList.toggle('active');
            body.classList.toggle('menu-open');
    
            if (burgerMenu.classList.contains('active')) {
              body.style.overflow = 'hidden';
            } else {
              body.style.overflow = '';
            }
          };
    
          burgerButton.addEventListener('click', toggleMenu);
    
          document.querySelectorAll('.burger-menu-content a').forEach(link => {
            link.addEventListener('click', (e) => {
              if (link.getAttribute('href') === '#') {
                e.preventDefault();
              }
              toggleMenu();
            });
          });
    
          overlay.addEventListener('click', toggleMenu);
    
          document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && burgerMenu.classList.contains('active')) {
              toggleMenu();
            }
          });
        }
      };
  
    const initSmoothScroll = () => {
      document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        if (anchor.getAttribute('href') !== '#') {
          anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
              e.preventDefault();
              target.scrollIntoView({ 
                behavior: 'smooth',
                block: 'start'
              });
            }
          });
        }
      });
    };
  
    initHorizontalScroll();
    initTabs();
    initBurgerMenu();
    initSmoothScroll();
  });