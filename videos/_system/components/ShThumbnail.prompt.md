The YouTube thumbnail — part of the system, not a scene.

```jsx
<ShThumbnail words={['Skip','This','Step']} accentIndex={0} aspect="9x16" width={300} />
```

Cream, three words or fewer, ink text with clay on one word. No face, no emoji, no border. On 9:16 the text sits in the top 40%.

**Not a composition component.** This belongs to `04-assets/thumbnail.png`
production (a still image, packaged separately for YouTube), never mounted
inside a rendered composition. Named explicitly here so nobody wires it into
a scene emitter by mistake.
