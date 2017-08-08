import Vue from 'vue'
import Router from 'vue-router'

//导入组件
import Index from '@/components/Index'
import Side from '@/components/Side'

Vue.use(Router)

export default new Router({
	routes: [
		{
			path: '/',
			name: 'IndexRoute',
			component: Index
		},{
			path: '/side',
			name: 'SideRoute',
			component: Side
		}
	]
})
