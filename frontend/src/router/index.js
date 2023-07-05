import { createRouter, createWebHistory } from 'vue-router'
import HomeImage from '../views/HomeImage.vue'

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: '/',
			component: HomeImage
		},
		{
			path: '/history',
			component: () => import('../views/HistoryImage.vue')
		},
	],
})

export default router
