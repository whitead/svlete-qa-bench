<script>
	import Answer from "./Answer.svelte";
	import data from "./data.js";

	let questions = new Set(data.map((m) => m.question));
	let selectedQuestion = questions.values().next().value;
</script>

<main>
	<h1 class="hero">qa_bench</h1>
	<div>by andrew white</div>

	<select bind:value={selectedQuestion}>
		{#each [...questions] as question, index}
			<option value={question}>Q{index + 1}</option>
		{/each}
	</select>
	<p>
		{selectedQuestion}
	</p>
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
		max-width: 1200px;
	}
</style>
