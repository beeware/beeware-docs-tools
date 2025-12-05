You might have the best software in the world - but if nobody knows how to use it, what's the point? Documentation can always be improved - and we need your help!

## Documentation form basics { #docs-form }

{{ formal_name }}'s documentation is written using [MkDocs and Markdown](https://www.markdownguide.org/basic-syntax/). We aim to follow the [Diataxis](https://diataxis.fr) framework for structuring documentation.

The Diataxis framework consists of a quadrant of four forms of documentation. Our interpretation of it is as follows:

- Tutorial - A guided learning experience, with a specific project endpoint.
- How-to guide - Instructions that guide the reader towards a specific goal or outcome.
- Topic guide - A discussion of a single idea, explained in such a way that the underlying concepts are clear.
- Reference - Technical descriptions of specific APIs or other interfaces.

## Choosing the right form

Before beginning a documentation contribution, it's important to identify which form is the best fit.

A tutorial is an introduction, particularly one focused at beginners, the goal of which should be getting them from a clean starting point to a finished product. It requires very specific instructions, and detailed explanations putting the information in context. You must assume nothing about the reader's experience with the tool being explained, although it's acceptable to assume some basic Python proficiency. There should be regular checkpoints where the reader can establish that they have succeeded in doing what you've described, and the success criteria should be clear. Known failure cases should also be clearly outlined, including explanations of any likely errors or problems the reader might experience. Things that change as a result of actions the reader has taken should be pointed out even if seemingly obvious toy you. Repetition is encouraged, especially if you're trying to establish a best practice or common processes. Explanations of internals should be avoided, as should alternative paths to the same outcome. A tutorial on baking cookies would be a specific set of instructions who has never baked before, and would need to account for things that an experienced baker would take for granted, such as the actual process of pre-heating the oven, or how long the cookies should be left to cool before eating.

A how-to guide should focus on a specific real-world use-case, and practical outcomes, not theoretical explanations. Unlike a tutorial, you can assume some familiarity with existing tools; the reader should be able to follow the guide from beginning to end and reach the goal, but they may need to have some existing knowledge to do so. It should include a set of concrete instructions or logical steps that need to be followed. A recipe is a good example of a how-to guide; there are many recipes for chocolate chip cookies, and they will all share common features, but any specific recipe should be possible to follow from beginning to end, and result in a consistent outcome. A good chocolate chip cookie recipe won't digress into the relative merits of different types of sugar or flour; it will include only the ingredients and instructions for baking a batch of cookies.

A topic guide describes a single subject or idea. It may include example code or instructions, but it is much more focused on providing a high-level picture of an overall landscape. It may include opinions and alternate perspectives, but the focus on the specific topic of the guide should be maintained. A topic guide on baking cookies might dig into the history of cookies as a baked product, explore that way that industrialized processes result in different types of cookies compared to homemade cookies, or suggest ways that cookies can be introduced into a broader diet.

Reference documentation is information oriented, describing specifics of operation of a tool library. They can quite often be generated from the code itself, but good API documentation may require further explanations and context. While it may sometimes include examples of usage, detailed explanations should be avoided. A reference guide in baking might describe the types of sugar that could be used, and detail their properties when used in baking. It would describe literal facts about sugar, but a broader discussion about choosing between sugar types should be the subject of a how-to or topic guide. The nutritional information found on most packaged foods would be considered reference documentation.

So, which form is the best fit for your contribution? Chances are a tutorial is not the right choice. You are most likely looking to submit a how-to or topic guide. Regardless, don't worry, we can help you narrow it down and choose during the proposal process.

## Documentation style

{{ formal_name }}'s documentation follows the guidelines outlined in the [documentation style guide](docs_style_guide.md). This guide includes basic style and formatting, and the process for the spelling check. It also covers various Markdown syntax details, such as reference link syntax, tips for working with code blocks, and image handling.

## Contributing documentation

{% macro content(template) %}{% include template %}{% endmacro %}
{% macro indented(template) %}{{ content(template)|indent }}{% endmacro %}

??? abstract "Proposing new documentation"

    {{ indented("feature_proposal.md") }}

??? abstract "Building documentation"

    {{ indented("docs_build.md") }}

??? abstract "Writing documentation"

    {{ indented("docs_contribute.md") }}
