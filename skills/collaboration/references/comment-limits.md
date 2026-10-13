# Comment limits and connector constraints

Research checked 2026-10-13. API support evolves; confirm what the current
connector exposes. These are comment-specific constraints, not document or
spreadsheet cell-size limits. Prefer the stricter of the service limit, connector
limit, and the session's conservative posting budget.

## Google Sheets: observed length rejection

A user reported this error while writing a Sheets comment:

> Comment cannot exceed the original 4000-character limit.

This is observed runtime evidence (no public source URL available), not a
verified universal limit for every Google comment endpoint. The public guides
reviewed below do not specify that exact limit or its counting unit.

- Treat 4,000 as a conservative ceiling for this workflow; target at most
  **3,500 UTF-16 code units** in each completed, signed comment or reply.
- Count the signature, whitespace, newlines, full links, and continuation
  labels. Apply the check to edits too, not just new comments.
- UTF-16 is a cautious local measurement: an emoji outside the BMP usually
  takes two units. It is not evidence that Google's server uses that unit.
- If an endpoint or connector documents a stricter or byte-based limit, use
  that limit and unit. Do not confuse JSON encoding overhead with text length.
- Shorten first. Only split into a few coherent replies when necessary; sign
  and preflight every part. Never resend the identical rejected payload.

Use the same 3,500-unit safety budget for Google Docs/Drive comments unless the
specific operation's supported limit is verified. Do not describe this policy
as a documented Google-wide 4,000-character maximum.

## Native Sheets comments versus Drive comments

The [Sheets comments guide](https://developers.google.com/workspace/sheets/api/guides/comments)
documents native cell coordinates, threads, and reply operations. Those may not
yet be exposed by the connector in the session.

- Native Sheets reads omit comments by default. Request comments and anchors
  explicitly (`commentsViewMode` and the relevant response fields) when using
  this API. Map anchors to the actual sheet and cell coordinates.
- Reads filtered to a range or sheet omit unanchored threads. A narrow read
  is not evidence that the rest of the spreadsheet has no comments.
- Comment writes can fail while other changes in the same batch are committed.
  Inspect `commentUpdateState`, not just HTTP success: `ALL_SAVED` confirms
  comment persistence; `ALL_FAILED_UNKNOWN_REASON` does not. Read back before
  repeating any part of the batch, especially already-saved cell edits.
- Only edit posts authored by the acting account. Since agents may share that
  account with the user, native authorship alone does not authorize changing
  the user's own comments; preserve the session's scope and agent attribution.

The [Drive comments guide](https://developers.google.com/workspace/drive/api/guides/manage-comments)
documents a different API surface:

- Google Workspace editors treat custom Drive API anchors as **unanchored**.
  An arbitrary Drive `anchor` does not create a visible native cell or text
  selection anchor. Name the precise tab/cell/passage in the comment if this
  is the supported, agreed workflow; do not claim native anchoring.
- Drive comment operations other than delete require the `fields` parameter.
  Include the fields needed to verify content, replies, and status.
- Follow pagination on comments and replies as needed. Deleted comments do
  not return their former text; do not claim to have read it.

## Document-wide Google comment limits

[Google's comments help](https://support.google.com/docs/answer/65129?hl=en)
documents a separate document-wide comment limit and a copy-based continuation
workflow. The help does not provide a numeric quota in the reviewed material.

Do not mistake this for a single-comment length error. Do not automatically
resolve/delete threads or make a replacement document to recover: that changes
history and the shared target. Explain the blocker and obtain agreement on a
continuation workflow. Splitting text does not solve a document-wide limit.

## Notion

The [Notion request limits](https://developers.notion.com/reference/request-limits)
apply to structured comment payloads too:

- `rich_text[].text.content`: at most **2,000 characters per text element**,
  not a claimed 2,000-character total comment limit.
- Rich-text arrays: at most **100 elements**. URLs: at most **2,000 characters**.
  The overall request-size ceiling is **500 KB**.
- A connector accepting one plain string may have a lower effective ceiling
  than a REST payload exposing multiple rich-text elements. Do not assume it
  splits text for you. If constructing supported rich-text objects, split at
  safe text boundaries within the *same comment* and preserve formatting and
  the final signature; still validate the array and whole request.
- Rate-limit responses require honoring `Retry-After` with bounded retries.
  Size/validation failures require changing the request, not backoff alone.
  A timed-out or failed write may already have saved; inspect before replaying.

The [create-comment reference](https://developers.notion.com/reference/create-a-comment)
and [comments guide](https://developers.notion.com/guides/data-apis/working-with-comments)
also distinguish capability and targeting constraints:

- Read-comment and insert-comment capabilities must be enabled separately;
  content-edit access is not proof of either capability.
- The current create endpoint documents page comments, whole-block comments,
  and replies to existing discussions. It cannot start a discussion on a
  selected text range inside a block. Connector/API-version support can lag.
- Choose the supported target explicitly; use an existing `discussion_id`
  when replying, not a new unrelated page-level comment.
- Comment Markdown supports inline formatting, not structured headings,
  fenced code blocks, lists, or tables. Do not assume body-document formatting
  is supported in comments.
- Read coverage may be limited to open comments and a specific page/block.
  Follow pagination and read relevant child-block discussions when supported.
  Do not infer rejected/accepted history from threads the connector cannot read.
