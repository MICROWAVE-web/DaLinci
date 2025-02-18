import fs from 'fs'
import path from 'path'
import postcss from 'postcss'
import tailwind from '../src/index'
import config from '../stubs/defaultConfig.stub.js'

function dropTailwindHeader(css) {
  let [header, ...lines] = css.split('\n')

  expect(
    /\/*! tailwindcss v\d*\.\d*\.\d* \| MIT License \| https:\/\/tailwindcss.com \*\//g.test(header)
  ).toBe(true)

  return lines.join('\n')
}

it('generates the right CSS using the default settings', () => {
  const inputPath = path.resolve(`${__dirname}/fixtures/tailwind-input.css`)
  const input = fs.readFileSync(inputPath, 'utf8')

  return postcss([tailwind()])
    .process(input, { from: inputPath })
    .then((result) => {
      const expected = fs.readFileSync(
        path.resolve(`${__dirname}/fixtures/tailwind-output.css`),
        'utf8'
      )

      expect(dropTailwindHeader(result.css)).toBe(dropTailwindHeader(expected))
    })
})

it('generates the right CSS when "important" is enabled', () => {
  const inputPath = path.resolve(`${__dirname}/fixtures/tailwind-input.css`)
  const input = fs.readFileSync(inputPath, 'utf8')

  return postcss([tailwind({ ...config, important: true })])
    .process(input, { from: inputPath })
    .then((result) => {
      const expected = fs.readFileSync(
        path.resolve(`${__dirname}/fixtures/tailwind-output-important.css`),
        'utf8'
      )

      expect(dropTailwindHeader(result.css)).toBe(dropTailwindHeader(expected))
    })
})

it('generates the right CSS when using @import instead of @tailwind', () => {
  const inputPath = path.resolve(`${__dirname}/fixtures/tailwind-input-import.css`)
  const input = fs.readFileSync(inputPath, 'utf8')

  return postcss([tailwind()])
    .process(input, { from: inputPath })
    .then((result) => {
      const expected = fs.readFileSync(
        path.resolve(`${__dirname}/fixtures/tailwind-output.css`),
        'utf8'
      )

      expect(dropTailwindHeader(result.css)).toBe(dropTailwindHeader(expected))
    })
})

it('generates the right CSS when enabling flagged features', () => {
  const inputPath = path.resolve(`${__dirname}/fixtures/tailwind-input.css`)
  const input = fs.readFileSync(inputPath, 'utf8')

  return postcss([
    tailwind({
      future: 'all',
      experimental: 'all',
    }),
  ])
    .process(input, { from: inputPath })
    .then((result) => {
      const expected = fs.readFileSync(
        path.resolve(`${__dirname}/fixtures/tailwind-output-flagged.css`),
        'utf8'
      )

      expect(dropTailwindHeader(result.css)).toBe(dropTailwindHeader(expected))
    })
})

it('generates the right CSS when color opacity plugins are disabled', () => {
  const inputPath = path.resolve(`${__dirname}/fixtures/tailwind-input.css`)
  const input = fs.readFileSync(inputPath, 'utf8')

  return postcss([
    tailwind({
      ...config,
      corePlugins: {
        textOpacity: false,
        backgroundOpacity: false,
        borderOpacity: false,
        placeholderOpacity: false,
        divideOpacity: false,
      },
    }),
  ])
    .process(input, { from: inputPath })
    .then((result) => {
      const expected = fs.readFileSync(
        path.resolve(`${__dirname}/fixtures/tailwind-output-no-color-opacity.css`),
        'utf8'
      )

      expect(dropTailwindHeader(result.css)).toBe(dropTailwindHeader(expected))
    })
})

it('does not add any CSS if no Tailwind features are used', () => {
  return postcss([tailwind()])
    .process('.foo { color: blue; }', { from: undefined })
    .then((result) => {
      expect(result.css).toMatchCss('.foo { color: blue; }')
    })
})

it('generates the right CSS with implicit screen utilities', () => {
  const inputPath = path.resolve(
    `${__dirname}/fixtures/tailwind-input-with-explicit-screen-utilities.css`
  )
  const input = fs.readFileSync(inputPath, 'utf8')

  return postcss([tailwind()])
    .process(input, { from: inputPath })
    .then((result) => {
      const expected = fs.readFileSync(
        path.resolve(`${__dirname}/fixtures/tailwind-output-with-explicit-screen-utilities.css`),
        'utf8'
      )

      expect(result.css).toBe(expected)
    })
})

it('generates the right CSS when "important" is enabled', () => {
  const inputPath = path.resolve(`${__dirname}/fixtures/tailwind-input.css`)
  const input = fs.readFileSync(inputPath, 'utf8')

  return postcss([tailwind({ ...config, important: true })])
    .process(input, { from: inputPath })
    .then((result) => {
      const expected = fs.readFileSync(
        path.resolve(`${__dirname}/fixtures/tailwind-output-important.css`),
        'utf8'
      )

      expect(dropTailwindHeader(result.css)).toBe(dropTailwindHeader(expected))
    })
})
