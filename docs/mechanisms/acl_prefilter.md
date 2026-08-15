# Pre-filter beats post-filter

Post-filter: retrieve 8, drop the ones the tenant cannot see. A denied neighbor can still take a slot and leak through a bug.

Pre-filter: the allowed-id set is a stencil on the index before search. A denied chunk never enters ANN and never enters the prompt.

The audit row is the proof: the denied id is absent.
