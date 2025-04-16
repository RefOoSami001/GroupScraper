particlesJS('particles-js', {
    "particles": {
        "number": {
            "value": 50,
            "density": {
                "enable": true,
                "value_area": 1000
            }
        },
        "color": {
            "value": ["#38bdf8", "#22d3ee", "#0ea5e9"]
        },
        "shape": {
            "type": "circle",
            "stroke": {
                "width": 0
            }
        },
        "opacity": {
            "value": 0.4,
            "anim": {
                "enable": true,
                "speed": 1,
                "opacity_min": 0.2
            }
        },
        "size": {
            "value": 3,
            "random": true
        },
        "move": {
            "enable": true,
            "speed": 0.5,
            "direction": "bottom",
            "out_mode": "out"
        }
    },
    "interactivity": {
        "events": {
            "onhover": {
                "enable": false
            }
        }
    },
    "retina_detect": true
});

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
}); 