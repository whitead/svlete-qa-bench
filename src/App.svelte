<script>
	import Answer from "./Answer.svelte";
	import data from "./data.js";

	let questions = new Set(data.map((m) => m.question));
	let selectedQuestion = questions.values().next().value;
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
		<p class="question">
			{selectedQuestion}
		</p>
	</div>
	<div class="answer-grid">
	{#each data.filter((m) => m.question === selectedQuestion) as entry}
    <Answer
      question={entry.question}
      model={entry.model}
      date={entry.date}
      answer={entry.answer}
      sources={entry.sources}
    />
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
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
		grid-gap: 20px;
		width: 80%;
		margin-bottom: 2rem;
	}
	
	.question {
		font-size: 1.5em;
		margin-left: 10px;
	}

	.question-container {
		display: flex;
		align-items: center;
	}

	@media (max-width: 900px) {
		.question-container {
			flex-direction: column;
			margin-top: 1rem;
		}

		.answer-grid {
			width: 90%;
			grid-template-columns: unset;
		}
	}

</style>
