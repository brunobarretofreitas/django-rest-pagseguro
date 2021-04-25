from xml.etree import ElementTree


def parse_session_id(xml_content: str) -> str:
    """
    Parser responsável por coletar o id da sessão da resposta XML
    da Pague Seguro

    Exemplo:
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <session>
        <id>1589121f381c4d4db1f12982b8ed1d62</id>
    </session>

    Parameters:
        xml_content (str): Retorno XML do endpoint de criar sessão

    Returns:
        session (str): Código da sessão criada
    """
    root = ElementTree.fromstring(xml_content)
    return root[0].text
