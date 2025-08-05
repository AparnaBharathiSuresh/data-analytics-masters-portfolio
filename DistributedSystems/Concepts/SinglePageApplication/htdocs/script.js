document.addEventListener('DOMContentLoaded', () => {
    setupSPA();
    setupPageHits();
    setupMouseEvents();
});

function setupSPA() {
    const links = document.querySelectorAll('a');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = e.target.getAttribute('href');

            // Allow external links and PDFs to work normally
            if (href.startsWith('http') || href.endsWith('.pdf')) {
                return; // Let the browser handle external links and PDFs
            }

            e.preventDefault(); // Prevent default anchor behavior for SPA links

            // Manage the SPA state and load content
            if (href === 'web/') {
                history.pushState({ page: 'web' }, 'web', 'WebProgramming');
                loadWebProgrammingPage();
            } else if (href === 'index.html' || href === '/') {
                history.pushState({ page: 'home' }, null, '/');
                loadMainPage();	
            } else {
                // Handle unknown links: show "Page Not Found" in the .main section
                history.pushState({ page: 'not-found' }, null, 'not-found');
                loadPageNotFound(); // Load 404 inside the main content area
            }
        });
    });

    // Handle forward/backward navigation with History API
    window.onpopstate = function(event) {
        if (event.state) {
            switch (event.state.page) {
                case 'web':
                    loadWebProgrammingPage();
                    break;
                case 'home':
                    loadMainPage();
                    break;
                case 'not-found':
                default:
                    loadPageNotFound();
                    break;
            }
        } else {
            // Handle case where there's no state (e.g., initial page load)
            loadMainPage();
        }
    };
}


function loadMainPage() {
    const url = 'index.html';

    // Clear existing content before loading new page
    document.querySelector('.main').innerHTML = '';

    // Remove WebProgramming.css if it exists
    loadCSS('WebProgramming.css', 'remove');

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            document.querySelector('.main').innerHTML = doc.querySelector('.main').innerHTML;
            document.querySelector('.sidebar').innerHTML = doc.querySelector('.sidebar').innerHTML;
        })
        .catch(error => {
            console.error('Error loading Main page:', error);
            loadPageNotFound();
        });
}


function loadWebProgrammingPage() {
    const mainContent = document.querySelector('.main');

    if (!mainContent) {
        console.error('Error: .main element not found');
        return;
    }

    const url = 'WebProgramming.html'; // Correct URL to fetch the actual file

    // Clear existing content before loading new page
    mainContent.innerHTML = ''; 

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html'); 
            mainContent.innerHTML = doc.body.innerHTML;
            
            // Ensure WebProgramming.css is loaded
            loadCSS('WebProgramming.css', 'add');
        })
        .catch(error => {
            console.error('Error loading Web Programming page:', error);
            loadPageNotFound();
        });
}


function loadPageNotFound() {
    const mainContent = document.querySelector('.main');
    
    if (mainContent) {
        mainContent.innerHTML = `
            <h1>404 - Page Not Found</h1>
            <p>Sorry, the page you are looking for does not exist.</p>
        `;
    } else {
        console.error('Error: .main element not found');
    }
}


function loadCSS(cssFile, action = 'add') {
    const existingLink = document.querySelector(`link[href="${cssFile}"]`);

    if (action === 'add') {
        // Only load the CSS file if it's not already loaded
        if (!existingLink) {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = cssFile;
            link.classList.add('dynamic-css'); // Add a class for dynamic CSS files
            document.head.appendChild(link);
        }
    } else if (action === 'remove') {
        // Remove the CSS file if it exists
        if (existingLink) {
            existingLink.remove();
        }
    }
}

function setupPageHits() {
    if (localStorage.pageHits) {
        localStorage.pageHits = Number(localStorage.pageHits) + 1;
    } else {
        localStorage.pageHits = 1;
    }
    const pageHitsElement = document.createElement('p');
    pageHitsElement.textContent = `Page visited ${localStorage.pageHits} times.`;
    document.querySelector('.main').appendChild(pageHitsElement);
}

// Mouse Events: Focus, Blur, and Hover
function setupMouseEvents() {
    const links = document.querySelectorAll('a');

    links.forEach(link => {
        // Hover effect (mouse over/out)
        link.addEventListener('mouseover', () => {
            link.style.backgroundColor = 'lightblue';
        });

        link.addEventListener('mouseout', () => {
            link.style.backgroundColor = '';
        });

        // Focus effect (keyboard navigation)
        link.addEventListener('focus', () => {
            link.style.outline = '2px solid blue';
        });

        link.addEventListener('blur', () => {
            link.style.outline = '';
        });
    });
}
