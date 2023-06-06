<script>
	import AnswerGroup from "./AnswerGroup.svelte";
	import data from "./data.js";
	// first strip https off model names
	data.forEach((d) => {
		d.model = d.model.replace("https://", "");
	});
	let questions = new Set(data.map((m) => m.question));
	let models = new Set(data.map((m) => m.model.split("-")[0]));
	let selectedQuestion = questions.values().next().value;
	let groupedAnswers = Object();
	questions.forEach((q) =>
		models.forEach((m) => {
			if (groupedAnswers[q] === undefined) groupedAnswers[q] = [];
			const a = data
				.flatMap((e) => {
					if (e.question === q && e.model.split("-")[0] === m)
						return e;
				})
				.filter((e) => e !== undefined);
			if (a.length > 0) groupedAnswers[q].push(a);
		})
	);
</script>

<main>
	<h1 class="hero">qa_bench</h1>
	<div>by andrew white</div>
	<div class="question-container">
		<select bind:value={selectedQuestion}>
			{#each [...questions] as question, index}
				<option value={question}>Q{index + 1}</option>
			{/each}
		</select>
		<p class="question">{selectedQuestion}</p>
	</div>
	<div class="answer-grid">
		{#each groupedAnswers[selectedQuestion].filter((g) => g.length > 0) as group}
			<AnswerGroup {group} />
		{/each}
	</div>
</main>

<style>
	main {
		display: flex;
		flex-direction: column;
		align-items: center;
	}

	.hero {
		font-size: 40px;
		margin: 20px;
	}

	.answer-grid {
		display: flex;
		align-items: flex-start;
		grid-gap: 20px;
		width: 80%;
		margin-bottom: 2rem;
		flex-wrap: wrap;
	}

	.question {
		font-size: 1.5em;
		margin-left: 10px;
	}

	.question-container {
		display: flex;
		align-items: center;
		width: 80%;
	}

	@media (max-width: 900px) {
		.question-container {
			flex-direction: column;
			margin-top: 1rem;
		}

		.answer-grid {
			width: 90%;
			display: grid;
		}
	}
</style>
