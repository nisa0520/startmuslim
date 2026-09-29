<script setup>
import { onBeforeUnmount, onMounted } from 'vue'

let revealObserver
let pageObserver

onMounted(() => {
	if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return

	const appRoot = document.querySelector('#app')
	if (!appRoot) return

	revealObserver = new IntersectionObserver((entries, observer) => {
		entries.forEach((entry) => {
			if (!entry.isIntersecting) return
			entry.target.classList.add('is-visible')
			observer.unobserve(entry.target)
		})
	}, { threshold: 0.12, rootMargin: '0px 0px -32px 0px' })

	const scanForRevealTargets = () => {
		const cardSelector = 'main.landing-page .problem-list > .card, main.landing-page .grid > .card, main.landing-page .different-grid > .different-card, main.landing-page .faq-list > .faq-item'
		const targets = appRoot.querySelectorAll(
			`${cardSelector}, main.landing-page .hero-copy > *, main.landing-page > section:not(.hero-wrap) h2, main.landing-page > section:not(.hero-wrap) h3, main.landing-page > section:not(.hero-wrap) p, main.landing-page > section:not(.hero-wrap) li, main.landing-page > section:not(.hero-wrap) summary, main.placement-page > section > *, main.auth-form-wrap > *, main.dash > *, footer.site-footer h2, footer.site-footer h3, footer.site-footer p, footer.site-footer li`,
		)
		const siblingCounts = new Map()
		targets.forEach((target) => {
			const isCardTarget = target.matches(cardSelector)
			if (!isCardTarget && target.closest('.card, .faq-item')) return
			if (target.classList.contains('scroll-reveal')) return
			const siblingIndex = siblingCounts.get(target.parentElement) || 0
			siblingCounts.set(target.parentElement, siblingIndex + 1)
			target.style.setProperty('--reveal-delay', `${Math.min(siblingIndex, 5) * 100}ms`)
			target.classList.add('scroll-reveal')
			revealObserver.observe(target)
		})
	}

	scanForRevealTargets()
	pageObserver = new MutationObserver(scanForRevealTargets)
	pageObserver.observe(appRoot, { childList: true, subtree: true })
})

onBeforeUnmount(() => {
	pageObserver?.disconnect()
	revealObserver?.disconnect()
})
</script>

<template><RouterView :key="$route.fullPath" /></template>
