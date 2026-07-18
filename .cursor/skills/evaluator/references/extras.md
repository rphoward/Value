(def-ref extras
  (linked-from protocol-4-optional)

  (section discovery-tags
    (when "Total Score is 95 or above")
    (emit "six hashtags after Final Score table")
    (quality "tasteful, curiosity-arousing, appropriate to work's mode, subject, and emotional register")
    (forbidden 'engagement-bait 'trending-style-tags)
    (format "horizontal, single space between each")
    (example artifact discovery-tags-example)
    (purpose "help a reader who would genuinely value this work discover it — not manufacture attention from those who wouldn't"))

  (section title-assessment
    (when "Total Score is 90 or above and Primary Mode is Narrative")
    (append "title assessment after Discovery Tags")
    (method "evaluate existing title (if present) against three criteria"
      (criterion 1 voice-fit "Could this title exist inside the prose style identified during analysis? Minimalist story needs minimalist title; ornate story earns ornate title.")
      (criterion 2 semantic-load "Does the title carry meaning that transforms after reading? Best titles are plain before and heavy after.")
      (criterion 3 autonomy "Does the title respect the reader's choice to engage or not? No bait, no manipulation, no false urgency."))
    (if-existing-scores-well "say so")
    (if-not "suggest up to three alternatives, each with one-sentence rationale")
    (check "all suggested titles must pass Fix Validation — speakable inside voice profile established during analysis")
    (format artifact title-assessment-format)
    (purpose "titles help the right reader find the work; first act of the voice, not a marketing decision")))

;; --- artifacts ---

## discovery-tags-example

`#DomesticRealism #QuietHorror #LaborAndLoss #MinimalistFiction #AmericanShortStory #TheThingsWeCannotSay`

## title-assessment-format

```
TITLE ASSESSMENT:
  Current: "[title]" — [brief evaluation]
  Alternatives (if warranted):
    1. "[title]" — [rationale]
    2. "[title]" — [rationale]
    3. "[title]" — [rationale]
```
