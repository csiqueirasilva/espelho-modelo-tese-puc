-- Converte macros básicas em blocos para Pandoc
local macros = {
  autor          = "author",
  titulo         = "title",
  subtitulo      = "subtitle",
  agradecimentos = "acknowledgments",
}

local function makeDiv(content, class)
  return pandoc.Div(content, {class = class})
end

function RawBlock(el)
  if el.format ~= "latex" then return nil end
  for macro, class in pairs(macros) do
    local found, body = el.text:match("\\" .. macro .. "%s*{(.-)}")
    if found then
      if macro == "titulo" then
        return makeDiv(pandoc.Header(1, body), class)
      else
        return makeDiv(pandoc.Para(body), class)
      end
    end
  end
end

function Header(el)
  if el.level == 1 then
    el.classes = {"Heading 1"}
  elseif el.level == 2 then
    el.classes = {"Heading 2"}
  elseif el.level == 3 then
    el.classes = {"Heading 3"}
  end
  return el
end

-- capturar legendas de figura
function Image(el)
  if el.caption and #el.caption > 0 then
    el.caption[1].classes = {"Caption"}
  end
  return el
end
