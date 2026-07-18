---
name: tool-ui-htmx
description: >
  Server-driven tool UI for forms, wizards, results, tables, and dense product
  views. Use when building or editing Twins presentation surfaces — Starlette
  routes/, Jinja templates, HTMX partials, or browser_assets for in-app UI.
  Python + Starlette + HTMX + Tailwind; minimal JS; optional islands only when
  earned. NOT for marketing homepages, heroes, portfolios, or landing-page
  redesigns (use design-taste-frontend).
disable-model-invocation: false
metadata:
  activation: path-and-intent
  paths: eliotapp/presentation/**
---

(def-sop tool-ui-htmx
  (context
    (target "presentation-tool-ui-agent")
    (optimization "server-driven-fragments-structure-before-style-preflight-gated")
    (scope "forms wizards results tables dense in-app views — NOT marketing heroes portfolios landing pages")
    (references
      (preflight-checklist "references/preflight-checklist.md")))

  <central_idea>
  (center-of-gravity
    (invariant "Server owns state; HTML fragments are the UI; structure before Tailwind; run protocol-10-preflight before ship."))
  </central_idea>

  (protocol-0-brief-read
    (before-any-code
      (require "one line before code: task, density (calm vs cockpit), primary action")
      (forbidden 'jump-to-markup-without-brief)))

  (protocol-1-default-stack
    (detect-existing (read-project-files-before-adding-deps))
    (http 'starlette :routes-under presentation/routes/ :app-factory presentation/app.py)
    (responses 'HTMLResponse-from-starlette.templating.Jinja2Templates)
    (templates 'jinja :under presentation/templates/)
    (client-behavior 'htmx :sole-approved-layer)
    (styles 'tailwind-css)
    (islands (opt-in-only) (forbidden 'default-react-next-spa-shell))
    (forbidden 'second-client-behavior-layer 'scattered-inline-script 'json-to-dom-rebuild 'handlers-outside-presentation-routes))

  (protocol-2-fragment-contract
    (route-module per-feature :under presentation/routes/)
    (stable-wrapper-id per-updatable-region)
    (python-branch (request.headers.get HX-Request) (partial-vs-full-page))
    (multi-target (hx-swap-oob when-multiple-regions-update))
    (forbidden 'unstable-swap-targets 'client-side-template-rebuild 'fat-route-with-domain-or-persistence))

  (protocol-3-forms
    (structure (label-above-input) (error-below-field))
    (security (csrf-on-post t))
    (htmx (hx-indicator-on-async) (hx-target-and-swap-explicit))
    (forbidden 'placeholder-as-label 'silent-submit-failure 'client-only-domain-validation))

  (protocol-4-wizard
    (server-owns-step-index t)
    (get-renders-step post-advances-or-completes)
    (back-via-post not-browser-back-default)
    (state (hidden-fields-or-session) (document-choice-inline))
    (forbidden 'client-side-step-router 'wizard-as-spa))

  (protocol-5-states
    (empty (teach-next-action))
    (loading (skeleton-or-indicator))
    (error (inline-field-or-region))
    (actions (one-primary-per-view))
    (forbidden 'silent-failure 'blank-panel-with-no-guidance))

  (protocol-6-product-discipline
    (note "cherry-pick product register — not marketing patterns")
    (earned-familiarity (consistent-button-vocabulary) (consistent-form-pattern))
    (motion (css-state-transitions-only :duration-150-250ms))
    (modals (skeptical-default prefer-inline-or-dedicated-view))
    (forbidden 'hero-layout-in-tool-views 'bento-marketing-grids 'gsap-default))

  (protocol-7-island-gate
    (default 'no-js-module)
    (allow-only-when (htmx-cannot-express-with-reason) (one-mount-point) (comment-declares-ceiling))
    (forbidden 'island-without-documented-reason 'island-for-form-or-wizard-flow))

  (protocol-8-copy
    (use CONTEXT.md-when-present)
    (forbidden 'invented-domain-facts 'fake-metrics 'marketing-superlatives-in-tool-labels))

  (protocol-9-out-of-scope
    (defer-to ".cursor/skills/design-taste-frontend/"
      'marketing-homepages 'heroes 'portfolios 'landing-page-redesigns 'bento-grids 'gsap-scroll-storytelling))

  (protocol-10-preflight
    (mandatory t)
    (full-checklist "references/preflight-checklist.md")
    (matrix-summary
      (brief-read-declared)
      (stack-confirmed)
      (fragment-map-stable-ids-routing)
      (forms-csrf-labels-errors-indicator)
      (wizard-server-owns-step)
      (empty-loading-error-states)
      (one-primary-action)
      (domain-copy-from-context)
      (island-documented-if-present)
      (no-scattered-inline-js)
      (a11y-structure-focus-contrast)
      (reduced-motion-honored))
    (if-any-fail (fix-before-deliver))))
