<script lang="ts">
	import { writable, type Writable } from 'svelte/store';
	import { onMount } from 'svelte';

	interface Widget {
		id: number;
		text: string;
		x?: number;
		y?: number;
	}

	let inputText = '';
	let sidebarWidgets: Writable<Widget[]> = writable([]);
	let mainWidgets: Writable<Widget[]> = writable([]);
	let widgetId = 0;
	let inputTextBox: HTMLInputElement;

	onMount(() => {
		inputTextBox = document.getElementById('inputText') as HTMLInputElement;
		if (inputTextBox) inputTextBox.focus();
	});

	function addWidget() {
		if (inputText.trim()) {
			sidebarWidgets.update((current) => [...current, { id: widgetId++, text: inputText }]);
			inputText = '';
			if (inputTextBox) inputTextBox.focus();
		}
	}

	function handleDragStart(event: DragEvent, widget: Widget, source: string) {
		event.dataTransfer?.setData('application/json', JSON.stringify({ widget, source }));
	}

	function handleDrop(event: DragEvent) {
		const { widget, source } = JSON.parse(event.dataTransfer?.getData('application/json') || '{}');
		const rect = event.currentTarget.getBoundingClientRect();
		const x = event.clientX - rect.left;
		const y = event.clientY - rect.top;

		if (source === 'sidebar') {
			mainWidgets.update((current) => [...current, { ...widget, x, y, id: widgetId++ }]);
		} else {
			mainWidgets.update((current) => {
				return current.map((w) => (w.id === widget.id ? { ...w, x, y } : w));
			});
		}
	}

	function handleDropOnWidget(event: DragEvent, targetWidget: Widget) {
		event.preventDefault();
		const { widget, source } = JSON.parse(event.dataTransfer?.getData('application/json') || '{}');

		if (source === 'sidebar') {
			mainWidgets.update((current) => [
				...current,
				{ ...widget, x: targetWidget.x, y: targetWidget.y, id: widgetId++ }
			]);
		} else {
			mainWidgets.update((current) => {
				return current.map((w) =>
					w.id === widget.id ? { ...w, x: targetWidget.x, y: targetWidget.y } : w
				);
			});
		}

		console.log(`Widget dropped on ${targetWidget.text}`);
	}
</script>

<div class="container">
	<div class="sidebar">
		<div class="sidebar-header">
			<input
				type="text"
				bind:value={inputText}
				placeholder="Type a word"
				id="inputText"
				on:keypress={(e) => {
					if (e.key === 'Enter') {
						addWidget();
					}
				}}
			/>
			<button on:click={addWidget}>Add Widget</button>
		</div>
		<div>
			{#each $sidebarWidgets as widget (widget.id)}
				<div
					class="widget initial"
					draggable="true"
					on:dragstart={(e) => handleDragStart(e, widget, 'sidebar')}
				>
					{widget.text}
				</div>
			{/each}
		</div>
	</div>
	<div class="main" on:drop={handleDrop} on:dragover={(e) => e.preventDefault()}>
		{#each $mainWidgets as widget (widget.id)}
			<div
				class="widget"
				style="left: {widget.x}px; top: {widget.y}px;"
				draggable="true"
				on:dragstart={(e) => handleDragStart(e, widget, 'main')}
				on:drop={(e) => handleDropOnWidget(e, widget)}
				on:dragover={(e) => e.preventDefault()}
			>
				{widget.text}
			</div>
		{/each}
	</div>
</div>

<style>
	.container {
		display: flex;
		height: 100vh;
		overflow: hidden;
	}

	.sidebar {
		width: 20%;
		background-color: #f0f0f0;
		box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
		display: flex;
		flex-direction: column;
		overflow-y: auto; /* Enable vertical scrolling */
		position: relative;
	}

	.sidebar-header {
		background-color: #f0f0f0;
		padding: 10px;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
		position: sticky;
		top: 0;
		z-index: 1;
	}

	.main {
		width: 80%;
		padding: 10px;
		background-color: #ffffff;
		position: relative;
		overflow: hidden;
	}

	.widget {
		padding: 10px;
		background-color: #add8e6;
		border: 1px solid #000;
		cursor: grab;
		min-width: 100px;
		min-height: 50px;
		position: absolute;
	}

	.widget.initial {
		position: static;
		margin-bottom: 10px;
	}
</style>
