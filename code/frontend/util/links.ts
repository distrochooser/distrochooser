export const getExternalLink = (baseUrl: string, languageCode: string, choosableName: string, source: string, addPage: boolean) => {
  const needle = choosableName+ ";"
  const inputUrl = source.indexOf(needle) !== -1 ? source.replace(needle, "") : source;
  if (addPage) {
    const base = new URL(baseUrl)
    return new URL("/pages/link/" + languageCode+ "/" + encodeSourceForPage(inputUrl), base)
  }
  return new URL(inputUrl)
}

export const encodeSourceForPage = (source: string) => encodeURI(btoa(source))