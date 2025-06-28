# 3. General stack

Date: 2025-06-28

## Status

Accepted

## Context

The application requires a stack of frameworks to be used. In the past, there were several stacks utilized, such as:

- PHP and Bootstrap
- Node.js, Bootstrap and Rust
- Node.js, Vue, Skeleton.js and Django
- Node.js, Nuxt and Django

As an experiment, a monolithic Django approach was developed, but showed additional effort in handling the form management, resulting in larger functions to be implemented.
Thus, it resulted in a non feasible code, causing the approach to be aborted.

In the past, the application was based Vue.js and Nuxt, even while running on older versions. A migration from Nuxt 2 to Nuxt 3 was not attempted due to the differences
in the API. Another option was in switching to React.js due to gained knowledge in the past.

Even as it is quite large, the project will stay on Django for the time being due to it's maturity and easy to use.
   
## Decision

The project will stick to Vue.js and will be utilizing Nuxt.js v3. With this, proper usage of TypeScript will be also introduced to the project as these Frameworks tend to be 
TypeScript centered anyways

## Consequences

Learning of the new Nuxt.js and Vue.js API, including requirements to bound a new API, as described in the next ADR.