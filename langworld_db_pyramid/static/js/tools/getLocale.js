export default function getLocale() {
    if (window.location.href.includes('/en/')) return 'en';
    return 'ru'
}