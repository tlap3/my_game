// pythons.js - เครื่องยนต์สำรองแบบหลายช่องทาง
if (typeof window.AsyncPython === 'undefined') {
    const scripts = [
        "https://github.io",
        "https://jsdelivr.net",
        "https://github.io"
    ];
    
    scripts.forEach(src => {
        let s = document.createElement('script');
        s.src = src;
        s.async = true;
        document.head.appendChild(s);
    });
}
