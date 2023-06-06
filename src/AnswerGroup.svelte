<script>
  import Answer from "./Answer.svelte";
  export let group = [];

  $: modelDatePairs = group.map((m) => `${m.model} (${m.date})`);
  $: startPair = modelDatePairs[modelDatePairs.length - 1];
  $: selectedModel = startPair.split(" (")[0];
  $: selectedDate = startPair.split(" ")[1].slice(1, -1);
  function handler(event) {
    const selectedPair = event.target.value;
    selectedModel = selectedPair.split(" (")[0];
    selectedDate = selectedPair.split(" ")[1].slice(1, -1);
  }
</script>

<div class="answer-group">
  <label>Model & Date: </label>
  <select value={startPair} on:change={handler}>
    {#each modelDatePairs as pair}
      <option value={pair}>{pair}</option>
    {/each}
  </select>
  {#each group.filter((entry) => entry.model === selectedModel && entry.date === selectedDate) as entry}
    <Answer
      question={entry.question}
      model={entry.model}
      date={entry.date}
      answer={entry.answer}
      sources={entry.sources}
    />
  {/each}
</div>

<style>
  .answer-group {
    max-width: 49%;
  }
</style>
