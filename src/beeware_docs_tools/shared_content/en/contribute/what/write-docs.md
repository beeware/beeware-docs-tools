You might have the best software in the world - but if nobody knows how to use it, what's the point? Documentation can always be improved - and we need your help!

## Documentation forms { #docs-form }

{{ formal_name }}'s documentation is written using [MkDocs and Markdown](https://www.markdownguide.org/basic-syntax/). We aim to follow the [Diataxis](https://diataxis.fr) framework for structuring documentation.

The Diataxis framework describes four "forms" of documentation:

- **Tutorial** - A guided learning experience, with a specific project endpoint.
- **How-to guide** - Instructions that guide the reader towards a specific goal or outcome.
- **Topic guide** - A discussion of a single idea, explained in such a way that the underlying concepts are clear.
- **Reference** - Technical descriptions of specific APIs or other interfaces.

Before beginning any documentation contribution, it's important to identify which form is the best fit. Many documentation proposals will be initial described as a request for "a tutorial on X" - but in most cases, what is actually required is how-to, topic guide, or improved reference information.

As an example, consider the task of writing documentation about baking cookies.

### Tutorial

A tutorial is an introduction, particularly one focused at beginners, the goal of which should be getting the reader from a clean starting point to a finished product. It requires very specific instructions, and detailed explanations that put the tutorial steps in context. You must assume nothing about the reader's experience with the tool being explained, although it's reasonable to assume some basic Python proficiency.

The tutorial should contain regular checkpoints where the reader can establish that they have succeeded in doing what has been described. At each checkpoint, success criteria should be clear. Known failure cases should be clearly outlined, including explanations of any likely errors or problems the reader might experience. Things that change as a result of actions the reader has taken should be pointed out, even if seemingly obvious. Repetition is encouraged, especially if you're trying to establish a best practice or common processes. Explanations of internals should be avoided, as should alternative paths to the same outcome.

A tutorial on baking cookies is more than just a recipe. The instructions in a tutorial should be accessible to someone who has never baked before (such as a child), and would need to account for things that an experienced baker would take for granted, such as how to cream sugar and butter, the process of pre-heating the oven, or how long cookies should be left to cool before eating. The goal of the tutorial isn't to produce a cookie - it's to convey the fundamentals of baking. The resulting cookie is the tasty treat that convinces someone to undertake the tutorial in the first place.

### How-to guide

A how-to guide should focus on a specific real-world use-case and practical outcomes, rather than theoretical explanations. Unlike a tutorial, you can assume some familiarity with existing tools. The reader should be able to follow the guide from beginning to end and reach the goal, but they may need some existing knowledge to do so. It should include a set of concrete instructions or logical steps that need to be followed to achieve the goal of the guide.

A recipe in a cookbook is a good example of a how-to guide. There are many recipes for chocolate chip cookies, and they will all share common features, but any specific recipe should be possible to follow from beginning to end, and result in a consistent outcome. A good chocolate chip cookie recipe won't digress into the relative merits of different types of sugar or flour, or give detailed instructions on basic technique or process; it will include only the ingredients and instructions for baking a batch of cookies, assuming the reader has basic familiarity with baking.

### Topic guide

A topic guide describes a single subject or idea. It may include example code or instructions, but it is much more focused on providing a high-level picture of an overall concept. It may include opinions and alternate perspectives, but the focus on the specific topic of the guide should be maintained.

A topic guide on baking cookies might dig into the history of cookies as a baked product, explore that way that industrialized processes result in different types of cookies compared to homemade cookies, or suggest ways that cookies can be incorporated into a balanced diet. By itself, it wouldn't be a very useful document to follow if you wanted to bake a cookie, but it might provide the background that would enable someone familiar with baking to successfully customize an existing cookie recipe.

### Reference

Reference documentation is information oriented, describing specifics of operation of a tool library. They can quite often be generated from the code itself, but good API documentation may require further explanations and context. While it may sometimes include examples of usage, detailed explanations should be avoided.

A reference guide in baking might describe the types of sugar that could be used, and detail their properties when used in baking. It would describe literal facts about sugar, but a broader discussion about choosing between sugar types should be the subject of a how-to or topic guide. The nutritional information found on most packaged foods would be considered reference documentation.

## Documentation style

{{ formal_name }}'s documentation follows the guidelines outlined in the [documentation style guide](../style/docs-style-guide.md). This guide includes basic style and formatting, and the process for the spelling check. It also covers various Markdown syntax details, such as reference link syntax, tips for working with code blocks, and image handling.

## Contributing documentation

/// details-abstract | Proposing new documentation

{% include "contribute/how/propose-feature.md" %}

///

/// details-abstract | Set up a development environment

{% include "contribute/how/dev-environment.md" %}

///

/// details-abstract | Work from a branch

{% include "contribute/how/branches.md" %}

///

/// details-abstract | Avoid scope creep

{% include "contribute/how/scope-creep.md" %}

///

/// details-abstract | Building documentation

{% include "contribute/how/build-docs.md" %}

///

/// details-abstract | Writing documentation

{% include "contribute/how/write-docs.md" %}

///

/// details-abstract | Add a change note

{% include "contribute/how/change-note.md" %}

///

/// details-abstract | Submit a pull request

{% include "contribute/how/submit-pr.md" %}

///
