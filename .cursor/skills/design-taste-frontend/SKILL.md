---
name: design-taste-frontend
description: Anti-slop frontend for landing pages, portfolios, and marketing-site redesigns. Use whenever the user builds or refreshes a homepage, hero, portfolio, or marketing page — or says the UI looks templated, generic, AI-generated, or "slop" — even if they never name a style. Covers Awwwards, Linear-style, editorial, and premium-consumer aesthetics. Audit-first on redesigns; pre-flight before ship. NOT for dashboards, admin panels, data tables, dense product UI, or multi-step wizards.
paths: eliotapp/presentation/browser_assets/**
disable-model-invocation: false
metadata:
  activation: intent-driven
---

(def-sop design-taste-frontend
  (context
    (target "frontend-design-agent")
    (optimization "anti-slop-contextual-protocols-audit-first-preflight-gated")
    (scope "landing pages portfolios redesigns — NOT dashboards data-tables multi-step-product-ui admin panels")
    (references
      (motion-skeletons "references/motion-skeletons.md")
      (appendices "references/appendices.md")
      (appendices-artifacts "references/appendices-artifacts.md")
      (preflight-checklist "references/preflight-checklist.md")
      (protocols-layout-motion "references/protocols-layout-motion.md — protocols 4-11")))

  <central_idea>
  (center-of-gravity
    (invariant "Every rule is contextual. Read the brief, infer direction, set three dials, then pull only matching protocols. None fire automatically. Run protocol-14-preflight before declaring done."))
  </central_idea>

  (protocol-0-brief-inference
    (before-any-code
      (read-signals
        (page-kind 'landing-saas 'landing-consumer 'landing-agency 'portfolio-dev 'portfolio-designer 'redesign-preserve 'redesign-overhaul 'editorial)
        (vibe-words user-stated-aesthetic)
        (reference-signals urls screenshots named-products competing-brands)
        (audience b2b-procurement design-conscious-consumer recruiter-scan)
        (brand-assets logo color type photography)
        (quiet-constraints a11y-first public-sector regulated trust-first-commerce kids-products))
      (quiet-constraints-override-aesthetic-preference t))
    (output-design-read
      (require "one line before code: Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <system or aesthetic family>.")
      (forbidden 'jump-to-default-aesthetic-without-read))
  (if (ambiguous-and-divergent?)
      (query-human :count 1 :example "Should this feel closer to Linear-clean or Awwwards-experimental?")
      (when confident (proceed-with-declared-read)))
    (anti-default-discipline
      (forbidden-as-default
        'ai-purple-gradients 'centered-hero-dark-mesh 'three-equal-feature-cards
        'generic-glassmorphism-everywhere 'infinite-loop-micro-animations-everywhere
        'inter-plus-slate-900)))

  (protocol-1-three-dials
    (variables
      (DESIGN_VARIANCE 8 "1=symmetry 10=artsy-chaos")
      (MOTION_INTENSITY 6 "1=static 10=cinematic")
      (VISUAL_DENSITY 4 "1=gallery-airy 10=cockpit-packed"))
    (baseline "8/6/4 unless design-read overrides — conversationally not by editing this file")
    (forbidden-aliases 'LAYOUT_VARIANCE 'ANIM_LEVEL)
    (dial-inference-table
      (minimalist-clean-calm-editorial-linear (variance 5-6) (motion 3-4) (density 2-3))
      (premium-consumer-apple-luxury (variance 7-8) (motion 5-7) (density 3-4))
      (playful-awwwards-experimental-agency (variance 9-10) (motion 8-10) (density 3-4))
      (landing-portfolio-marketing-default (variance 7-9) (motion 6-8) (density 3-5))
      (trust-first-public-sector-regulated (variance 3-4) (motion 2-3) (density 4-5))
      (redesign-preserve (variance match-existing) (motion +1) (density match-existing))
      (redesign-overhaul (variance +2) (motion +2) (density match-existing)))
    (use-case-presets
      (landing-saas (7 6 4))
      (landing-agency (9 8 3))
      (landing-premium-consumer (7 6 3))
      (portfolio-designer (8 7 3))
      (portfolio-developer (6 5 4))
      (editorial-blog (6 4 3))
      (public-sector (3 2 5))
      (redesign-preserve (match match+1 match))
      (redesign-overhaul (+2 +2 match))))

  (protocol-2-design-system-map
    (honesty-rule "brief matches a named system → install official package; one system per project; no hand-rolled recreation")
    (official-systems
      (microsoft-enterprise '@fluentui/react-components '@fluentui/web-components)
      (google-material '@material/web)
      (ibm-b2b '@carbon/react '@carbon/styles)
      (shopify-app 'polaris.js)
      (atlassian '@atlaskit/* '@atlaskit/tokens)
      (github-devtool '@primer/css '@primer/react-brand)
      (uk-public-sector 'govuk-frontend)
      (us-public-sector 'uswds)
      (agency-mvp 'bootstrap-5.3)
      (accessible-react '@radix-ui/themes)
      (own-components 'shadcn/ui :never-ship-default-state)
      (indie-saas-marketing 'tailwind-v4 :dark-variant))
    (aesthetic-not-system
      (implement "native CSS + Tailwind + maintained components; label inspiration vs official in comments")
      (families 'glassmorphism 'bento-grid 'brutalism 'editorial 'dark-tech 'aurora-mesh 'kinetic-type
                :apple-liquid-glass "web approximation only — see references/appendices-artifacts.md"))
    (install-and-docs "references/appendices.md for maps; appendices-artifacts.md for bash/css"))

  (protocol-3-default-architecture
    (unless-official-system-from-protocol-2
      (stack
        (framework 'react-or-next :default-rsc)
        (rsc-safety "providers and global state in use-client wrapper only")
        (interactivity-isolation "motion scroll listeners pointer physics → isolated client leaf")
        (styling 'tailwind-v4 :v3-only-if-project-demands)
        (tailwind-v4-postcss "@tailwindcss/postcss or Vite plugin — not tailwindcss plugin in postcss.config.js")
        (animation 'motion/react :legacy-alias framer-motion)
        (fonts 'next/font-or-self-host :forbidden "Google Fonts link in production"))
      (state
        (local 'useState 'useReducer)
        (global-only-when-needed 'zustand 'jotai 'react-context)
        (forbidden "useState for continuous pointer/scroll values — use useMotionValue useTransform useScroll"))
      (icons
        (priority '@phosphor-icons/react 'hugeicons-react '@radix-ui/react-icons '@tabler/icons-react)
        (discouraged 'lucide-react :unless user-or-project-already-uses)
        (forbidden 'hand-rolled-svg-icons 'mixing-icon-families)
        (standardize strokeWidth globally))
      (emoji (discouraged-default) (override-only "playful chat social-native brief"))
      (layout
        (breakpoints sm-640 md-768 lg-1024 xl-1280 2xl-1536)
        (container "max-w-[1400px] or max-w-7xl mx-auto")
        (viewport "min-h-[100dvh] for heroes — never h-screen")
        (grid-over-flex-math "CSS Grid not calc flex percentages"))
      (dependency-verification "check package.json before any import; output install command if missing")))

  (protocol-4-through-11
    (reference "references/protocols-layout-motion.md" -- design engineering, motion, a11y, dials, dark mode, AI tells, vocabulary, redesign))

  (protocol-12-block-library-contract
    (status "schema defined; blocks added iteratively")
    (location "skills/taste-skill/blocks/<category>/<name>.md")
    (frontmatter-required name category dial_compatibility when_to_use not_for stack)
    (body-required
      visual-sketch props-api code-sketch mobile-fallback motion-variants dark-mode-notes anti-patterns references)
    (discipline "one block per file standalone passes protocol-14; system variants suffix --system"))

  (protocol-13-out-of-scope
    (not-for 'dashboards 'data-tables 'multi-step-wizards 'code-editors 'native-mobile 'realtime-collab)
    (when-brief-matches "say so; point to Section 2 system; apply marketing surfaces only"))

  (protocol-14-preflight-check
    (mandatory t)
    (full-checklist "references/preflight-checklist.md")
    (matrix-summary
      (brief-inference-declared)
      (dial-values-explicit-reasoned)
      (design-system-chosen-or-aesthetic-labeled)
      (redesign-mode-audited-if-applicable)
      (zero-em-dashes)
      (page-theme-lock)
      (color-consistency-lock)
      (shape-consistency-lock)
      (button-contrast-cta-wrap-form-contrast)
      (serif-discipline-premium-palette-ban)
      (italic-descender-clearance)
      (hero-viewport-padding-stack-discipline)
      (eyebrow-count-mechanical)
      (split-header-ban zigzag-cap duplicate-cta-intent)
      (logo-wall-under-hero-real-svg logo-only)
      (bento-rhythm-cell-count background-diversity)
      (copy-self-audit motion-motivated marquee-max-one)
      (nav-single-line section-layout-repetition)
      (long-lists-right-component real-images-no-fake-screenshots)
      (no-production-test-tells-from-protocol-9)
      (motion-claimed-shown gsap-canonical reduced-motion)
      (no-window-scroll-listener dark-mode-both-tested mobile-collapse)
      (min-h-100dvh useEffect-cleanup empty-loading-error-states)
      (icons-allowed-only no-ai-tells cwv-plausible one-design-system))
    (if-any-fail (fix-before-deliver))))
