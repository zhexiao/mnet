<template>
	<div id="app">
		<md-toolbar>
			<md-button class="md-icon-button">
				<md-icon>menu</md-icon>
			</md-button>

			<h2 class="md-title" style="flex: 1">Mnet</h2>

			<md-button class="md-icon-button">
				<md-icon>favorite</md-icon>
			</md-button>
		</md-toolbar>
		<router-view></router-view>
	</div>
</template>

<script>
	export default {
		name: 'app'
	}
</script>
