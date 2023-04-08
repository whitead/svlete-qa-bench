<script>
	import Answer from "./Answer.svelte";
	import data from "./data.js";

	let questions = data.map((m) => m.question);
	let selectedQuestion = questions[0];
</script>

<main>
	<h1 class="hero">qa_bench</h1>

	<select bind:value={selectedQuestion}>
		{#each [...questions] as question}
			<option value={question}>{question}</option>
		{/each}
	</select>
	<div>author: andrew</div>
	{#each data.filter((m) => m.question === selectedQuestion) as entry}
    <Answer
      question={entry.question}
      model={entry.model}
      date={entry.date}
      answer={entry.answer}
      sources={entry.sources}
    />
  {/each}
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

	.prompt {
		font-size: 20px;
		color: #fff;
		margin: 20px;
	}
</style>
