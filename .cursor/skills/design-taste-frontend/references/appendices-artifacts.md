(def-ref appendices-artifacts
  (linked-from design-system-appendix)
  (artifact install-commands-bash)
  (artifact liquid-glass-css))

## install-commands-bash

```bash
npm install @material/web
npm install @fluentui/react-components
npm install @fluentui/web-components @fluentui/tokens
npm install @carbon/react @carbon/styles
npm install @radix-ui/themes
npx shadcn@latest init
npx shadcn@latest add button card badge separator input
npm install --save @primer/css
npm install @primer/react-brand
npm install govuk-frontend
npm install uswds
yarn add @atlaskit/css-reset @atlaskit/tokens @atlaskit/button @atlaskit/badge @atlaskit/section-message @atlaskit/card
npm install bootstrap
# Shopify Polaris: meta shopify-api-key + cdn shopifycloud/polaris.js
```

## liquid-glass-css

Not official. Label as web glassmorphism approximation in comments. No `liquid-glass.css` from Apple.

```css
.liquid-glass-web-approx {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  border-radius: 999px;
  border: 1px solid rgb(255 255 255 / .32);
  background:
    linear-gradient(135deg, rgb(255 255 255 / .30), rgb(255 255 255 / .08)),
    rgb(255 255 255 / .12);
  backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  -webkit-backdrop-filter: blur(24px) saturate(180%) contrast(1.05);
  box-shadow:
    inset 0 1px 0 rgb(255 255 255 / .48),
    inset 0 -1px 0 rgb(255 255 255 / .12),
    0 18px 60px rgb(0 0 0 / .18);
}

@media (prefers-color-scheme: dark) {
  .liquid-glass-web-approx {
    border-color: rgb(255 255 255 / .18);
    background:
      linear-gradient(135deg, rgb(255 255 255 / .16), rgb(255 255 255 / .04)),
      rgb(15 23 42 / .42);
  }
}

@media (prefers-reduced-transparency: reduce) {
  .liquid-glass-web-approx {
    background: rgb(255 255 255 / .96);
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
}
```

Always provide contrast without blur. Test `prefers-reduced-transparency` (uneven browser support).
