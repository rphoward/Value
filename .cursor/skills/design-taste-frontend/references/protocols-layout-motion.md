(def-ref design-taste-protocols-layout-motion
  (linked-from protocol-4-design-engineering protocol-5-context-aware-proactivity protocol-6-performance-accessibility protocol-7-dial-definitions protocol-8-dark-mode protocol-9-ai-tells protocol-10-reference-vocabulary protocol-11-redesign))

  (protocol-4-design-engineering
    (typography
      (display-default "text-4xl md:text-6xl tracking-tighter leading-none")
      (body-default "text-base text-gray-600 leading-relaxed max-w-[65ch]")
      (sans-discouraged-default 'Inter :override "neutral Linear-style or public-sector brief")
      (pairings-know 'Geist+Geist-Mono 'Satoshi+JetBrains-Mono 'Cabinet-Grotesk+Inter-Tight)
      (serif-discipline
        (very-discouraged-as-default t)
        (allowed-only-when
          (brand-names-serif-font)
          (or editorial-luxury-publication-manuscript-heritage-with-articulated-fit))
        (default-sans-display 'Geist-Display 'Cabinet-Grotesk-Display 'PP-Neue-Montreal)
        (emphasis "italic or bold SAME family — never random serif word in sans headline")
        (banned-defaults 'Fraunces 'Instrument_Serif)
        (if-justified-rotate-pool 'PP-Editorial-New 'GT-Sectra 'Cormorant 'Playfair 'Canela))
      (italic-descender-clearance "leading-[1.1] min + pb-1 when italic has y g j p q in display type"))
    (color
      (max-one-accent saturation-under-80-percent-default)
      (lila-rule "no default AI purple/blue glow — override when brand asks purple with intent")
      (one-palette-per-project "no warm/cool gray mix")
      (color-consistency-lock "one accent whole page")
      (premium-consumer-palette-ban
        (banned-default-families
          (backgrounds '#f5f1ea '#f7f5f1 '#fbf8f1 '#efeae0 '#ece6db '#faf7f1 '#e8dfcb)
          (accents '#b08947 '#b6553a '#9a2436 '#9c6e2a '#bc7c3a '#7d5621)
          (text '#1a1714 '#1a1814 '#1b1814))
        (rotate-alternatives 'cold-luxury 'forest 'black-and-tan 'cobalt-cream 'terracotta-slate 'olive-brick 'monochrome-pop)
        (rotation-rule "never ship beige+brass twice in a row for premium-consumer")))
    (layout-diversification
      (anti-center-bias "when DESIGN_VARIANCE > 4 prefer split asymmetric pinned — centered OK for editorial manifesto launch"))
    (materiality
      (cards-only-for-real-hierarchy)
      (shadows "tint to background hue not pure black")
      (density-over-7 "no generic card containers for metrics")
      (shape-consistency-lock "one radius system or documented rule everywhere"))
    (interactive-states
      (require 'loading-skeleton 'empty 'error 'tactile-active-feedback)
      (button-contrast-wcag-aa)
      (cta-wrap-ban "one line at desktop; 3 words max primary; widen not wrap")
      (no-duplicate-cta-intent "one label per intent page-wide")
      (form-contrast-wcag-aa))
    (forms (label-above-input) (error-below) (forbidden 'placeholder-as-label))
    (layout-discipline-hard-rules
      (hero-viewport-fit "headline ≤2 lines subtext ≤20 words ≤4 lines CTA visible")
      (hero-font-scale "text-4xl md:text-5xl lg:text-6xl default; text-6xl+ only 3-5 word headlines")
      (hero-top-padding-max "pt-24 desktop")
      (hero-stack-max-4 "eyebrow-or-brand-strip headline subtext CTAs — ban tagline trust-strip pricing bullets in hero")
      (logo-wall-under-hero-not-in)
      (nav-single-line-desktop height-max-80px)
      (bento-rhythm-and-exact-cell-count "N items → N cells no empty tiles")
      (section-layout-repetition-ban "layout family once per page; 8 sections → ≥4 families")
      (zigzag-cap "max 2 consecutive image+text splits")
      (eyebrow-restraint "max 1 per 3 sections; mechanical count uppercase tracking labels")
      (split-header-ban "no left headline + right floater paragraph — stack vertically")
      (bento-background-diversity "≥2-3 cells need image gradient pattern tint")
      (mobile-collapse-explicit-per-section))
    (images
      (priority-1 'image-gen-tool-when-available)
      (priority-2 'picsum-seed-or-brand-urls)
      (priority-3 'labeled-placeholder-slots-and-tell-user)
      (minimalist-still-needs-images "≥2-3 real images")
      (logo-wall 'simple-icons-or-devicon-or-generated-svg-monogram :logo-only-no-category-labels)
      (forbidden 'div-fake-screenshots 'hand-rolled-decorative-svg-default))
    (content-density
      (section-shape "headline ≤8 words sub ≤25 words one visual or CTA")
      (long-lists "not default ul divide-y for >5 — cards tabs carousel marquee etc")
      (spec-sheets "no border-b every row — card grid grouped chunks featured-vs-rest")
      (copy-self-audit "re-read every visible string; fix grammar unclear AI cute")
      (fake-precise-numbers "real labeled-mock or banned")
      (one-copy-register-per-page))
    (quotes "≤3 lines body; typographic quotes or none; no em-dash in quote")
    (page-theme-lock "one light dark or auto whole page — section flip banned unless deliberate once"))

  (protocol-5-context-aware-proactivity
    (note "tools not defaults — pull when design-read calls")
    (glassmorphism "premium consumer Apple-adjacent; inner border + inset shadow; prefers-reduced-transparency fallback")
    (magnetic-physics "MOTION_INTENSITY > 5 + premium/playful; useMotionValue only")
    (perpetual-micro "MOTION_INTENSITY > 5 when section benefits; not every card loops; spring physics")
    (motion-claimed-motion-shown "MOTION_INTENSITY > 4 must animate or drop dial to 3")
    (motion-motivated "hierarchy storytelling feedback state-transition — one sentence reason or drop")
    (marquee-max-one-per-page)
    (gsap-patterns "sticky-stack horizontal-pan — see references/motion-skeletons.md start top top pin true")
    (forbidden-animation
      (forbidden 'window-scroll-listener-in-react 'scrollY-in-useState 'raf-touching-react-state)
      (allowed 'motion-useScroll 'gsap-ScrollTrigger 'IntersectionObserver 'css-scroll-driven-animations)
      (layout-transitions 'motion-layout-layoutId-for-real-state-changes-only)
      (stagger 'staggerChildren-or-css-cascade-delay)))

  (protocol-6-performance-accessibility
    (animate-only 'transform 'opacity)
    (reduced-motion "MOTION_INTENSITY > 3 must honor prefers-reduced-motion — non-negotiable")
    (dark-mode-mandatory-consumer "both modes from start; tailwind dark: or CSS variables one strategy")
    (cwv-targets (LCP "<2.5s") (INP "<200ms") (CLS "<0.1") (run-lighthouse))
    (dom-cost "grain on fixed pointer-events-none pseudo only; lazy-load below-fold heavy libs")
    (z-index-restraint "document scale in constants file"))

  (protocol-7-dial-definitions
    (DESIGN_VARIANCE
      (1-3 "symmetrical 12-col equal padding centered")
      (4-7 "overlaps varied aspect ratios offset headers")
      (8-10 "masonry fractional grid massive whitespace")
      (mobile "<768 collapse asymmetric to single column"))
    (MOTION_INTENSITY
      (1-3 "hover active only")
      (4-7 "fluid CSS transitions transform opacity")
      (8-10 "scroll reveals parallax GSAP — never window scroll listener"))
    (VISUAL_DENSITY
      (1-3 "py-32 to py-48 gallery spacing")
      (4-7 "py-16 to py-24 app spacing")
      (8-10 "tight 1px lines font-mono numbers")))

  (protocol-8-dark-mode
    (token-strategy-one 'tailwind-dark-variant 'css-semantic-variables)
    (enforce-contrast-hierarchy-brand-fidelity)
    (no-pure-000-or-fff)
    (default prefers-color-scheme unless brand insists)
    (test-both-modes-before-finish))

  (protocol-9-ai-tells
    (visual (forbidden 'neon-outer-glows-default 'pure-black '#000 'oversaturated-accents 'gradient-text-headers 'custom-cursors))
    (typography (avoid-inter-default) (serif-only-editorial-luxury-not-dashboards))
    (layout (forbidden 'three-equal-feature-cards 'mathematically-perfect-floating-gaps))
    (content
      (forbidden 'John-Doe-names 'generic-avatars 'fake-perfect-99.99 'Acme-Nexus-SmartFlow
                 'Elevate-Seamless-Unleash-verbs))
    (resources
      (forbidden 'hand-rolled-icons 'div-fake-screenshots 'broken-unsplash 'shadcn-default-state))
    (production-test-tells
      (hero 'version-labels-v0-beta 'brand-no-01-sub-eyebrows)
      (sections 'numbered-eyebrows-00-index '01-4-pagination-on-tiles 'scroll-001-cues)
      (separators 'middle-dot-rationed-max-1-per-line 'decorative-status-dots)
      (typography-flourishes 'br-italic-headline-default 'rotated-vertical-text 'decorative-crosshair-grid)
      (fake-previews 'div-fake-dashboard-in-hero 'fake-version-footers-in-preview)
      (marketing-copy
        'quietly-in-use-at 'field-notes-poetic-labels 'weather-locale-strips 'micro-meta-under-eyebrows
        'stage-1-2-3-labels)
      (pills 'overlaid-image-tags 'pretentious-photo-credits 'version-footers-on-marketing
            'reservation-counters-decoration)
      (decoration 'hero-bottom-mono-strip-brand-motion-spatial 'floating-top-right-subtext-in-header)
      (lists 'border-t-and-b-every-row 'scoring-bars-with-filled-tracks)
      (locale-scroll 'city-time-weather-strips 'scroll-cues))
    (em-dash-ban
      (invariant "ZERO em-dash — or en-dash as separator — anywhere visible; use hyphen period comma parentheses")
      (preflight-fail-if-any-present t)))

  (protocol-10-reference-vocabulary
    (note "pattern names for communication — implementations in block library")
    (hero 'asymmetric-split 'editorial-manifesto 'video-mask 'kinetic-type 'curtain-reveal 'scroll-pinned)
    (nav 'dock-magnification 'magnetic-button 'gooey-menu 'dynamic-island 'mega-menu)
    (layout 'bento 'masonry 'chroma-grid 'split-screen-scroll 'sticky-stack)
    (cards 'parallax-tilt 'spotlight-border 'glassmorphism 'holographic-foil 'morphing-modal)
    (scroll 'sticky-stack 'horizontal-hijack 'zoom-parallax 'scroll-progress-path)
    (galleries 'coverflow 'drag-pan 'accordion-slider 'hover-trail)
    (type 'kinetic-marquee 'text-mask 'text-scramble 'circular-path 'gradient-stroke)
    (micro 'particle-button 'skeleton-shimmer 'directional-hover-fill 'mesh-gradient)
    (library-choice
      (motion/react "UI bento state")
      (gsap+ScrollTrigger "scrolltelling hijacks isolated client leaf cleanup")
      (three-js "canvas 3D isolated")
      (forbidden "mix GSAP/Three with Motion in same component tree")))

  (protocol-11-redesign
    (detect-mode 'greenfield 'redesign-preserve 'redesign-overhaul)
    (if-ambiguous (query-human-once "preserve brand or visual scratch?"))
    (audit-before-touch
      (document 'brand-tokens 'ia 'content-blocks 'patterns-preserve 'patterns-retire
                'dial-reading-existing 'seo-baseline))
    (preservation
      (keep-ia-slugs-nav-labels-unless-asked)
      (extract-brand-colors-before-protocol-4-color)
      (preserve-copy-voice 'honor-a11y-wins 'respect-analytics-event-names))
    (modernisation-levers-priority
      1-typography 2-spacing 3-color 4-motion 5-hero-recompose 6-full-block-replace)
    (never-change-silently 'url-slugs 'primary-nav-labels 'form-field-names 'logo 'legal-copy)
    (decision-tree
      (ia-content-seo-sound "targeted-evolution levers 1-4 ~70% value ~40% risk")
      (structural-visual-debt "full-redesign strict content preservation")
      (brand-changing "greenfield")))
