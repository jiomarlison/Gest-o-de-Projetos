import cv2
from flet import *
import shutil
import os
from datetime import datetime

ultima_rota = []
coordenadas = []


def main(page: Page):
    page.title = "BM face"

    def window_event(e):
        if e.data == "close":
            page.dialog = confirmacao_saida
            confirmacao_saida.open = True
            page.update()

    page.window_prevent_close = True
    page.on_window_event = window_event
    page.theme_mode = ThemeMode.LIGHT
    page.window_center()
    page.scroll = True
    page.window_min_width = 1000
    page.window_min_height = 600
    page.vertical_alignment = CrossAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.snack_bar = SnackBar(content=Text("Aviso"), action="Alright!", )

    def sim_click(e):
        page.window_destroy()

    def nao_click(e):
        confirmacao_saida.open = False
        page.update()

    confirmacao_saida = AlertDialog(
        modal=True,
        title=Text(
            "CONFIRMAR SAIDA?",
            weight=FontWeight.BOLD,
            color=colors.RED,
            italic=True,
        ),
        content=Text(
            value="DESEJA REALMENTE SAIR?\nQUALQUE ALTERAÇÃO NÃO SALVA SERÁ PERDIDA!",
            weight=FontWeight.BOLD,
            color=colors.BLACK,

        ),
        actions=[
            ElevatedButton("SIM", on_click=sim_click),
            OutlinedButton("NÃO", on_click=nao_click),
        ],
        actions_alignment=MainAxisAlignment.END,
    )
    gradiente = LinearGradient(
        begin=alignment.top_left,
        end=alignment.bottom_right,
        colors=[colors.RED_50, colors.BLUE_50, colors.TEAL_50],
    )

    lista_pacientes = os.listdir("assets/fotos pacientes")

    def GeradorNumeroIdentificacaoPaciente():
        return int(
            int(datetime.now().strftime("%Y%m%d")) + int(datetime.now().strftime("%H%M%S"))
            + int(datetime.now().strftime("%s")[-5:])
        )

    def verificarPaciente(e):
        if escolha_paciente is not None:
            for container in container_upload_fotos_paciente.content.controls:
                if container.key == "area_upload_fotos_paciente":
                    container.disabled = False
            page.update()

    escolha_paciente = Dropdown(
        padding=5,
        border_radius=5,
        height=page.window_height * 0.10 if page.window_height > 100 else 100,
        width=page.window_width - 100 if page.window_width > 100 else 100,
        options=[
            dropdown.Option(paciente)
            for paciente
            in sorted(lista_pacientes)
        ],
        on_change=verificarPaciente
    )

    def salvarFotosPaciente(e: FilePickerResultEvent):
        data_hoje = datetime.now().strftime("%Y-%m-%d")
        if not os.path.isdir(f'assets/fotos pacientes/{escolha_paciente.value}/{data_hoje}'):
            os.mkdir(f'assets/fotos pacientes/{escolha_paciente.value}/{data_hoje}')

        for imagen in e.files:
            nome_imagens.controls.append(
                Text(value=imagen.name, weight=FontWeight.BOLD)
            )
            minha_copia_imagens = os.path.join(
                os.getcwd(), f'assets/fotos pacientes/{escolha_paciente.value}/{data_hoje}'
            )
            shutil.copy(
                imagen.path, minha_copia_imagens
            )
            os.rename(
                src=f'assets/fotos pacientes/{escolha_paciente.value}/{data_hoje}/{imagen.name}',
                dst=f'assets/fotos pacientes/{escolha_paciente.value}/{data_hoje}/'
                    f'{datetime.now().strftime("%Y%m%d%H%M%S%f")}-{escolha_paciente.value}.'
                    f'{imagen.name.split(".")[-1]}'
            )
            page.update()
            nome_imagens.update()

    upload_arquivo = FilePicker(
        on_result=salvarFotosPaciente,
    )

    nome_imagens = Row()
    page.overlay.append(upload_arquivo)

    container_upload_fotos_paciente = Container(
        content=Column(
            controls=[
                Container(
                    padding=5,
                    border_radius=5,
                    height=page.window_height * 0.10 if page.window_height > 100 else 100,
                    width=page.window_width - 100 if page.window_width > 100 else 100,
                    alignment=alignment.center,
                    gradient=gradiente,

                    content=Row(
                        controls=[
                            IconButton(
                                icon=icons.HOME,
                                bgcolor=colors.BLUE_50,
                                on_click=lambda _: page.go("/telaInicialProfissional"),
                            ),
                            Text(
                                value="REALIZAR UPLOAD DAS FOTOS DO PACIENTE",
                                text_align=TextAlign.CENTER,
                                weight=FontWeight.BOLD,
                                size=int(page.window_width / page.window_height) * 30,
                            ),
                        ],
                        vertical_alignment=CrossAxisAlignment.CENTER,
                    ),
                    key='cabecalho_upload_fotos_paciente',
                ),
                escolha_paciente,
                Container(
                    padding=5,
                    border_radius=5,
                    height=page.window_height * 0.70 if page.window_height > 100 else 100,
                    width=page.window_width - 100 if page.window_width > 100 else 100,
                    alignment=alignment.center,
                    gradient=gradiente,
                    content=Column(
                        [
                            ElevatedButton(
                                text="Escolher fotos a salvar",
                                icon=icons.UPLOAD,
                                on_click=lambda e: upload_arquivo.pick_files(
                                    allow_multiple=True,
                                    allowed_extensions=['jpeg', 'jpg', 'png', ]
                                ),
                            ),
                            nome_imagens,
                        ],
                        alignment=MainAxisAlignment.CENTER,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                    key='area_upload_fotos_paciente',
                    disabled=True
                ),
            ]
        )
    )

    def eventosImagempaciente(image=None):
        def click_event(event, x, y, flags, params):
            if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_RBUTTONDOWN:
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, ".", (x, y), font,
                            0.5, (0, 0, 255), 2)
                cv2.imshow('imagem paciente', img)

        if image:
            img = cv2.imread(image, 1)
            cv2.imshow('imagem paciente', img)
            cv2.setMouseCallback('imagem paciente', click_event)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def TelaInicialAtendente(e):
        page.route = "/telaInicialAtendente"
        ultima_rota.clear()
        ultima_rota.append("/telaInicialAtendente")
        page.update()

    def TelaLoginProfissionais(e):
        page.route = "/telaInicialProfissional"
        ultima_rota.clear()
        ultima_rota.append("/telaInicialProfissional")
        page.update()

    def cadastrarNovoPaciente(e):
        id_paciente = GeradorNumeroIdentificacaoPaciente()
        os.mkdir(f"assets/fotos pacientes/{id_paciente}")
        page.snack_bar = SnackBar(
            content=Text(
                value="PACIENTE CADASTRADO COM SUCESSO!"
                      f"\nNº DE IDENTIFICAÇÃO: {id_paciente}",
                color=colors.BLACK,
                weight=FontWeight.BOLD,
                text_align=TextAlign.CENTER,
                selectable=True,
            ),
            action='DESFAZER',
            action_color=colors.BLACK,
            on_action=lambda _: os.rmdir(f"assets/fotos pacientes/{id_paciente}"),
            show_close_icon=True,
            close_icon_color=colors.RED_ACCENT_700,
            bgcolor=colors.BLUE_200,
            dismiss_direction=DismissDirection.HORIZONTAL,
        )
        page.snack_bar.open = True
        page.route = "/telaInicialAtendente"
        page.update()

    def cadastrarFicha(e):
        page.snack_bar = SnackBar(
            content=Text(
                value="Ficha do paciente cadastrada com sucesso!"
            ),
            duration=2000,
            bgcolor=colors.BLUE_200
        )
        page.snack_bar.open = True
        page.route = "/telaInicialProfissional"
        page.update()

    def cadastrarNovoProfissional(e):
        page.snack_bar = SnackBar(
            content=Text(
                value="PROFISSIONAL CADASTRADO COM SUCESSO!",
                color=colors.BLACK,
                weight=FontWeight.BOLD,
                text_align=TextAlign.CENTER,
                selectable=True,
            ),
            action='DESFAZER',
            action_color=colors.BLACK,
            show_close_icon=True,
            close_icon_color=colors.RED_ACCENT_700,
            bgcolor=colors.BLUE_200,
            dismiss_direction=DismissDirection.HORIZONTAL,
        )
        page.snack_bar.open = True
        page.route = "/telaInicialAtendente"
        page.update()

    def verFotoPaciente(e):
        page.route = "/fotosPaciente"
        page.update()

    def retornar(e):
        pasta_paciente.content = botoes_pacientes
        page.update()

    def foto_paciente(e):
        pasta_paciente.content = ResponsiveRow(
            controls={
                ElevatedButton(
                    text="Retornar",
                    on_click=retornar
                ),
                Text(
                    value=e.control.key,
                    color=colors.RED,
                    text_align=TextAlign.CENTER,
                ),
                Container(
                    image_src=f"assets/fotos pacientes/{e.control.key}",
                    image_fit=ImageFit.CONTAIN,
                    width=page.window_width - 200,
                    height=page.window_height - 200,
                    key=e.control.key,
                    on_click=lambda _: eventosImagempaciente(
                        f"assets/fotos pacientes/{e.control.key}"),
                    padding=10,
                    shadow=BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=colors.GREEN,
                        offset=Offset(0, 0),
                        blur_style=ShadowBlurStyle.OUTER,
                    )
                ),
            },
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )
        page.update()

    def fotos_dia_paciente(e):
        pasta_paciente.content = ResponsiveRow(
            controls=[
                ElevatedButton("Retornar", on_click=retornar),
                Column(
                    controls=[
                        ElevatedButton(
                            text=nome,
                            height=20,
                            width=page.window_width,
                            key=f'{e.control.key}/{nome}',
                            on_click=foto_paciente,
                        )
                        for nome
                        in os.listdir(fr"assets/fotos pacientes/{e.control.key}")
                    ]
                )
            ]
        )
        page.update()

    def abrir_fotos_pasta_paciente(e):
        id = e.control.key
        pasta_paciente.content = ResponsiveRow(
            controls=[
                ElevatedButton("Retornar", on_click=retornar),
                Row(
                    controls=[
                        ElevatedButton(
                            text=nome,
                            key=f'{e.control.key}/{nome}',
                            on_click=fotos_dia_paciente,
                        ) for nome in os.listdir(fr"assets/fotos pacientes/{e.control.key}")
                    ],
                    width=1000,
                    alignment=MainAxisAlignment.CENTER,
                ),
            ],
            expand=1,
            spacing=5,
            run_spacing=5,
        ) \
            if len(os.listdir(fr"assets/fotos pacientes/{e.control.key}")) > 0 \
            else \
            Container(
                content=Text(
                    value="Paciente sem foto cadastrada, retornar aos pacientes",
                    size=30,
                    text_align=TextAlign.CENTER,
                    color='black',
                    weight=FontWeight.BOLD,
                ),
                on_click=retornar,
                width=50,
                height=50,
                border_radius=5,
                bgcolor=colors.LIGHT_BLUE_50,
                alignment=alignment.center
            )
        page.update()

    botoes_pacientes = GridView(
        controls=[
            ElevatedButton(
                text=nome,
                icon=icons.FOLDER,
                key=nome,
                on_click=abrir_fotos_pasta_paciente
            ) for nome in sorted(list(os.listdir(r"assets/fotos pacientes")))
        ],
        expand=1,
        runs_count=8,
        child_aspect_ratio=5,

    )

    pasta_paciente = Container(
        content=botoes_pacientes,
        width=1000,
        height=600,
    )

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    Container(
                        content=Row(
                            controls=[
                                Image(
                                    src="assets/icon.png",
                                    width=100,
                                ),
                                Text(
                                    value="BM face",
                                    color=colors.WHITE,
                                    size=40,
                                    font_family="Open Sans",
                                    text_align=TextAlign.CENTER,
                                    weight=FontWeight.BOLD,
                                    width=600,
                                ),
                            ],
                        ),
                        width=800,
                        height=100,
                        bgcolor="#1a7fa0",
                        border_radius=5,
                        padding=2,
                        alignment=alignment.center,
                    ),
                    Container(
                        content=ResponsiveRow(
                            controls=[
                                Column(
                                    controls=[
                                        ElevatedButton(
                                            content=ResponsiveRow(
                                                controls=[
                                                    Row(
                                                        controls=[
                                                            Image(
                                                                src="assets/login_atendente.png",
                                                                height=60,
                                                                width=60,
                                                            ),
                                                            Text(
                                                                value="Atendente",
                                                                size=60,
                                                                color=colors.TEAL
                                                            ),
                                                        ],
                                                        alignment=MainAxisAlignment.CENTER
                                                    )
                                                ],
                                            ),
                                            width=650,
                                            height=150,
                                            on_click=lambda _: page.go("/loginAtendente"),
                                        ),
                                        ElevatedButton(
                                            content=ResponsiveRow(
                                                controls=[
                                                    Row(
                                                        controls=[
                                                            Image(
                                                                src="assets/login_medico.png",
                                                                height=60,
                                                                width=60,
                                                            ),
                                                            Text(
                                                                value="Profissional",
                                                                size=60,
                                                                color=colors.BLUE_900,
                                                            ),
                                                        ],
                                                        alignment=MainAxisAlignment.CENTER,
                                                    )
                                                ],

                                            ),
                                            width=650,
                                            height=150,
                                            on_click=lambda _: page.go("/loginProfissional")
                                        ),
                                    ],
                                    horizontal_alignment=CrossAxisAlignment.CENTER,
                                    scroll=ScrollMode.AUTO,
                                ),
                            ],
                        ),
                        width=800,
                        height=600,
                        border_radius=10,
                        gradient=gradiente,
                        alignment=alignment.center,
                    )
                ],
                horizontal_alignment=CrossAxisAlignment.CENTER,
                vertical_alignment=MainAxisAlignment.CENTER,
            )
        )
        if page.route == "/loginAtendente":
            page.views.append(
                View(
                    "/loginAtendente",
                    [
                        Container(
                            content=Row(
                                controls=[
                                    Image(
                                        src="assets/icon.png",
                                        width=100,
                                    ),
                                    Text(
                                        value="BM face",
                                        color=colors.WHITE,
                                        size=40,
                                        font_family="Open Sans",
                                        text_align=TextAlign.CENTER,
                                        weight=FontWeight.BOLD,
                                        width=600,
                                    ),
                                    IconButton(
                                        icon=icons.HOME,
                                        icon_color="#1a7fa0",
                                        bgcolor=colors.BLUE_50,
                                        width=100,
                                        on_click=lambda _: page.go("/"),
                                    )
                                ],
                                vertical_alignment=CrossAxisAlignment.CENTER,
                            ),
                            width=800,
                            height=100,
                            bgcolor="#1a7fa0",
                            border_radius=5,
                            alignment=alignment.center,
                            padding=2,
                        ),
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    Column(
                                        controls=[
                                            Image(
                                                src="assets/login_atendente.png",
                                                height=80,
                                                width=80,
                                            ),
                                            Text(
                                                value="Atendente",
                                                font_family="ARIAL",
                                                text_align=alignment.center,
                                                weight=FontWeight.BOLD,
                                                size=80,
                                            ),
                                            TextField(
                                                label="Usuário",
                                                hint_text="Digite sua Mátricula",
                                                icon=icons.PERSON,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=40,
                                                width=700,
                                                height=100,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Senha",
                                                hint_text="Digite sua senha",
                                                password=True,
                                                icon=icons.PASSWORD,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                can_reveal_password=True,
                                                text_size=40,
                                                width=700,
                                                height=100,
                                                border_radius=10,
                                            ),
                                            ElevatedButton(
                                                text="Fazer Login",
                                                icon=icons.LOGIN,
                                                icon_color=colors.GREEN,
                                                color=colors.BLACK,
                                                bgcolor=colors.LIGHT_BLUE_50,
                                                on_click=TelaInicialAtendente,
                                                width=200,
                                                height=50,
                                            )
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        scroll=ScrollMode.AUTO,
                                    ),
                                ],
                            ),
                            width=800,
                            height=600,
                            border_radius=10,
                            gradient=gradiente,
                        )
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                )
            )
            page.update()
        if page.route == "/loginProfissional":
            page.views.append(
                View(
                    "/loginProfissional",
                    [
                        Container(
                            content=Row(
                                controls=[
                                    Image(
                                        src="assets/icon.png",
                                        width=100,
                                    ),
                                    Text(
                                        value="BM face",
                                        color=colors.WHITE,
                                        size=40,
                                        font_family="Open Sans",
                                        text_align=TextAlign.CENTER,
                                        weight=FontWeight.BOLD,
                                        width=600,
                                    ),
                                    IconButton(
                                        icon=icons.HOME,
                                        icon_color="#1a7fa0",
                                        bgcolor=colors.BLUE_50,
                                        width=100,
                                        on_click=lambda _: page.go("/"),
                                    )
                                ],
                                vertical_alignment=CrossAxisAlignment.CENTER,
                            ),
                            width=800,
                            height=100,
                            bgcolor="#1a7fa0",
                            border_radius=5,
                            alignment=alignment.center,
                            padding=2,
                        ),
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    Column(
                                        controls=[
                                            Image(
                                                src="assets/login_medico.png",
                                                height=80,
                                                width=80,
                                            ),
                                            Text(
                                                value="Profissional",
                                                font_family="ARIAL",
                                                text_align=alignment.center,
                                                weight=FontWeight.BOLD,
                                                size=80,
                                            ),
                                            TextField(
                                                label="Usuário",
                                                hint_text="Digite seu CRM ou CRO",
                                                icon=icons.PERSON,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=40,
                                                width=700,
                                                height=100,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Senha",
                                                hint_text="Digite sua senha",
                                                password=True,
                                                icon=icons.PASSWORD,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                can_reveal_password=True,
                                                text_size=40,
                                                width=700,
                                                height=100,
                                                border_radius=10,
                                            ),
                                            ElevatedButton(
                                                text="Fazer Login",
                                                icon=icons.LOGIN,
                                                icon_color=colors.GREEN,
                                                color=colors.BLACK,
                                                bgcolor=colors.LIGHT_BLUE_50,
                                                on_click=TelaLoginProfissionais,
                                                width=200,
                                                height=50,
                                            )
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER,
                                        scroll=ScrollMode.AUTO,
                                    ),
                                ],
                            ),
                            width=800,
                            height=600,
                            border_radius=10,
                            gradient=gradiente,
                        )
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                )
            )
            page.update()
        if page.route == "/telaInicialAtendente":
            ViewTelaInicialAtendente = page.views.append(
                View(
                    "/telaInicialatendente",
                    [
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    Container(
                                        content=Row(
                                            controls=[
                                                IconButton(
                                                    icon=icons.HOME,
                                                    bgcolor=colors.BLUE_50,
                                                    on_click=lambda _: page.go("/"),
                                                ),
                                                Text(
                                                    value="Natália Albuquerque",
                                                    color=colors.WHITE,
                                                    size=40,
                                                    font_family="Open Sans",
                                                    text_align=TextAlign.CENTER,
                                                    weight=FontWeight.BOLD,
                                                    width=900,
                                                ),
                                            ],
                                            vertical_alignment=CrossAxisAlignment.CENTER,
                                        ),
                                        width=1000,
                                        height=100,
                                        bgcolor=colors.BLUE_ACCENT_200,
                                        border_radius=5,
                                        alignment=alignment.center,
                                        padding=10,
                                    ),
                                ]
                            ),
                            width=1000,
                            height=100,
                            border_radius=10,
                            gradient=gradiente,
                            alignment=alignment.center,
                            padding=2
                        ),
                        Text(
                            value="Procedimentos",
                            text_align=TextAlign.CENTER,
                            size=30,
                            weight=FontWeight.BOLD,
                        ),
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    GridView(
                                        controls=[
                                            DataTable(
                                                columns=[
                                                    DataColumn(Text("Data")),
                                                    DataColumn(Text("Paciente"), numeric=True),
                                                    DataColumn(Text("Profissional")),
                                                ],
                                                rows=[
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("22/04/2024")),
                                                            DataCell(Text("12345")),
                                                            DataCell(Text("00000000-0")),

                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("22/04/2024")),
                                                            DataCell(Text("23456")),
                                                            DataCell(Text("00000000-2233")),
                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("22/04/2024")),
                                                            DataCell(Text("34567")),
                                                            DataCell(Text("00000000-3344")),
                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("23/04/2024")),
                                                            DataCell(Text("67891")),
                                                            DataCell(Text("00000000-0")),

                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("23/04/2024")),
                                                            DataCell(Text("78911")),
                                                            DataCell(Text("00000000-2233")),
                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("23/04/2024")),
                                                            DataCell(Text("89111")),
                                                            DataCell(Text("00000000-3344")),
                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("23/04/2024")),
                                                            DataCell(Text("78911")),
                                                            DataCell(Text("00000000-2233")),
                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("23/04/2024")),
                                                            DataCell(Text("89111")),
                                                            DataCell(Text("00000000-3344")),
                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("23/04/2024")),
                                                            DataCell(Text("78911")),
                                                            DataCell(Text("00000000-2233")),
                                                        ]
                                                    ),
                                                    DataRow(
                                                        cells=[
                                                            DataCell(Text("23/04/2024")),
                                                            DataCell(Text("89111")),
                                                            DataCell(Text("00000000-3344")),
                                                        ]
                                                    ),

                                                ],
                                                border=border.all(1, "teal"),
                                                heading_row_color=colors.RED_100,
                                                border_radius=5,
                                            ),
                                        ],
                                        expand=True,
                                    ),
                                ],
                            ),
                            width=1000,
                            height=400,
                            border_radius=10,
                            gradient=gradiente,
                            alignment=alignment.top_center,
                            padding=2,
                            theme_mode=ThemeMode.SYSTEM,
                        ),
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    Row(
                                        controls=[
                                            ElevatedButton(
                                                content=Text(
                                                    value="Cadastrar novo paciente",
                                                    size=15,
                                                    weight=FontWeight.BOLD,
                                                ),
                                                height=50,
                                                width=200,
                                                on_click=lambda _: page.go("/cadastrarNovoPaciente")
                                            ),
                                            ElevatedButton(
                                                content=Text(
                                                    value="Pacientes ativos para consultas",
                                                    size=15,
                                                    weight=FontWeight.BOLD,
                                                ),
                                                height=50,
                                                width=200,
                                                on_click=lambda _: page.go("/listaPacientes")
                                            ),
                                            ElevatedButton(
                                                content=Text(
                                                    value="Cadastrar novo profissional",
                                                    size=15,
                                                    weight=FontWeight.BOLD,
                                                ),
                                                height=50,
                                                width=200,
                                                on_click=lambda _: page.go("/cadastrarNovoProfissional")
                                            ),
                                            ElevatedButton(
                                                content=Text(
                                                    value="Profissionais ativos para consultas",
                                                    size=15,
                                                    weight=FontWeight.BOLD
                                                ),
                                                height=50,
                                                width=200,
                                                on_click=lambda _: page.go("/listaProfissionais")
                                            ),
                                        ],
                                        alignment=MainAxisAlignment.CENTER
                                    )
                                ]
                            ),
                            width=1000,
                            height=100,
                            border_radius=10,
                            gradient=gradiente,
                            alignment=alignment.center,
                            padding=2
                        ),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    # scroll=ScrollMode.ALWAYS,
                ),
            )
        if page.route == "/telaInicialProfissional":
            ViewTelaInicialAtendente = page.views.append(
                View(
                    "/telaInicialProfissional",
                    [
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    Container(
                                        content=Row(
                                            controls=[
                                                IconButton(
                                                    icon=icons.HOME,
                                                    bgcolor=colors.BLUE_50,
                                                    on_click=lambda _: page.go("/"),
                                                ),
                                                Text(
                                                    value="Dr. Leonardo Castellani",
                                                    color=colors.WHITE,
                                                    size=40,
                                                    font_family="Open Sans",
                                                    text_align=TextAlign.CENTER,
                                                    weight=FontWeight.BOLD,
                                                    width=900,
                                                ),
                                            ],
                                            vertical_alignment=CrossAxisAlignment.CENTER,
                                        ),
                                        width=1000,
                                        height=100,
                                        bgcolor=colors.BLUE_ACCENT_200,
                                        border_radius=5,
                                        alignment=alignment.center,
                                        padding=10,
                                    ),
                                ]
                            ),
                            width=1000,
                            height=100,
                            border_radius=10,
                            alignment=alignment.center,
                            padding=2
                        ),
                        Column(
                            controls=[
                                Text(
                                    value="Procedimentos",
                                    text_align=TextAlign.CENTER,
                                    size=30,
                                    weight=FontWeight.BOLD,
                                ),
                                Container(
                                    content=ResponsiveRow(
                                        controls=[
                                            GridView(
                                                controls=[
                                                    DataTable(
                                                        columns=[
                                                            DataColumn(Text("Data")),
                                                            DataColumn(Text("Paciente"),
                                                                       numeric=True),
                                                            DataColumn(Text("Profissional")),
                                                        ],
                                                        rows=[
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("22/04/2024")),
                                                                    DataCell(Text("12345")),
                                                                    DataCell(Text("00000000-0")),

                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("22/04/2024")),
                                                                    DataCell(Text("23456")),
                                                                    DataCell(Text("00000000-2233")),
                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("22/04/2024")),
                                                                    DataCell(Text("34567")),
                                                                    DataCell(Text("00000000-3344")),
                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("23/04/2024")),
                                                                    DataCell(Text("67891")),
                                                                    DataCell(Text("00000000-0")),

                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("23/04/2024")),
                                                                    DataCell(Text("78911")),
                                                                    DataCell(Text("00000000-2233")),
                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("23/04/2024")),
                                                                    DataCell(Text("89111")),
                                                                    DataCell(Text("00000000-3344")),
                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("23/04/2024")),
                                                                    DataCell(Text("78911")),
                                                                    DataCell(Text("00000000-2233")),
                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("23/04/2024")),
                                                                    DataCell(Text("89111")),
                                                                    DataCell(Text("00000000-3344")),
                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("23/04/2024")),
                                                                    DataCell(Text("78911")),
                                                                    DataCell(Text("00000000-2233")),
                                                                ]
                                                            ),
                                                            DataRow(
                                                                cells=[
                                                                    DataCell(Text("23/04/2024")),
                                                                    DataCell(Text("89111")),
                                                                    DataCell(Text("00000000-3344")),
                                                                ]
                                                            ),

                                                        ],
                                                        border=border.all(1, "teal"),
                                                        heading_row_color=colors.RED_100,
                                                        border_radius=5,
                                                    ),
                                                ],
                                                expand=True,
                                            ),
                                        ],
                                    ),
                                    width=1000,
                                    height=400,
                                    border_radius=10,
                                    gradient=gradiente,
                                    alignment=alignment.top_center,
                                    padding=2,
                                    theme_mode=ThemeMode.SYSTEM,
                                ),
                            ],
                            horizontal_alignment=CrossAxisAlignment.CENTER
                        ),
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    Row(
                                        controls=[
                                            ElevatedButton(
                                                content=Text(
                                                    value="Pacientes ativos para consulta",
                                                    size=12,
                                                    weight=FontWeight.BOLD,
                                                ),
                                                height=50,
                                                width=180,
                                                on_click=lambda _: page.go("/listaPacientes")
                                            ),
                                            ElevatedButton(
                                                content=Text(
                                                    value="Capturar Foto Paciente",
                                                    size=12,
                                                    weight=FontWeight.BOLD
                                                ),
                                                height=50,
                                                width=180,
                                            ),
                                            ElevatedButton(
                                                content=Text(
                                                    value="Fotos paciente",
                                                    size=12,
                                                    weight=FontWeight.BOLD
                                                ),
                                                height=50,
                                                width=180,
                                                on_click=lambda _: page.go("/fotosPaciente")
                                            ),
                                            ElevatedButton(
                                                content=Text(
                                                    value="Cadastrar ficha de anamnese do paciente",
                                                    size=12,
                                                    weight=FontWeight.BOLD,
                                                ),
                                                height=50,
                                                width=180,
                                                on_click=lambda _: page.go("/cadastrarAnamnese")
                                            ),
                                            ElevatedButton(
                                                content=Text(
                                                    value="Fazer upload fotos paciente",
                                                    size=12,
                                                    weight=FontWeight.BOLD,
                                                ),
                                                height=50,
                                                width=180,
                                                on_click=lambda _: page.go("/uploadFotosPacientes")
                                            ),

                                        ],
                                        alignment=MainAxisAlignment.CENTER
                                    )
                                ]
                            ),
                            width=1000,
                            height=100,
                            border_radius=10,
                            gradient=gradiente,
                            alignment=alignment.center,
                            padding=2
                        ),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    # scroll=ScrollMode.ALWAYS,
                ),
            )
        if page.route == "/cadastrarNovoPaciente":
            page.views.append(
                View(
                    "/cadastrarNovopaciente",
                    [
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    Column(
                                        controls=[
                                            Container(
                                                content=Row(
                                                    controls=[
                                                        IconButton(
                                                            icon=icons.HOME,
                                                            bgcolor=colors.BLUE_50,
                                                            on_click=lambda _: page.go(ultima_rota[-1]),
                                                        ),
                                                        Text(
                                                            value="Cadastrar paciente",
                                                            color=colors.WHITE,
                                                            size=40,
                                                            font_family="Open Sans",
                                                            text_align=TextAlign.CENTER,
                                                            weight=FontWeight.BOLD,
                                                            width=900,
                                                        ),
                                                    ],
                                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                                ),
                                                width=1000,
                                                height=100,
                                                bgcolor=colors.BLUE_ACCENT_200,
                                                border_radius=5,
                                                alignment=alignment.center,
                                                padding=10,
                                            ),
                                            Icon(
                                                name=icons.PEOPLE,
                                                color=colors.RED,
                                                size=50
                                            ),
                                            TextField(
                                                label="Nome",
                                                hint_text="Digite o nome do paciente",
                                                icon=icons.ABC_ROUNDED,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=40,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Endereço",
                                                hint_text="Digite o endereço do paciente",
                                                icon=icons.HOUSE,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=40,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Email",
                                                hint_text="Digite o email do paciente",
                                                icon=icons.EMAIL,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=40,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Celular",
                                                hint_text="Digite o celular para contato do paciente",
                                                icon=icons.SMARTPHONE,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=40,
                                                border_radius=10,
                                            ),

                                            TextField(
                                                label="CPF",
                                                hint_text="Digite o CPF do paciente",
                                                icon=icons.ONETWOTHREE_ROUNDED,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=40,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Sexo",
                                                hint_text="sexo do paciente",
                                                icon=icons.GROUPS_2,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=40,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Data de Nascimento",
                                                hint_text="Digite a data de nascimento do paciente",
                                                icon=icons.CALENDAR_MONTH,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=40,
                                                border_radius=10,
                                            ),
                                            ElevatedButton(
                                                text="Realizar Cadastro",
                                                icon=icons.CHECK_CIRCLE,
                                                bgcolor=colors.LIGHT_GREEN_ACCENT_100,
                                                color=colors.BLACK,
                                                width=300,
                                                height=60,
                                                on_click=cadastrarNovoPaciente
                                            )
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                    ),
                                ]
                            ),
                            width=1000,
                            height=600,
                            border_radius=10,
                            gradient=gradiente,
                            alignment=alignment.top_center,
                            padding=2
                        ),
                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    # scroll=ScrollMode.ALWAYS,
                ),
            )
        if page.route == "/cadastrarNovoProfissional":
            page.views.append(
                View(
                    "//cadastrarNovoProfissional",
                    [
                        Container(
                            content=ResponsiveRow(
                                controls=[
                                    Column(
                                        controls=[
                                            Container(
                                                content=Row(
                                                    controls=[
                                                        IconButton(
                                                            icon=icons.HOME,
                                                            bgcolor=colors.BLUE_50,
                                                            on_click=lambda _: page.go(ultima_rota[-1]),
                                                        ),
                                                        Text(
                                                            value="Cadastrar profissional",
                                                            color=colors.WHITE,
                                                            size=40,
                                                            font_family="Open Sans",
                                                            text_align=TextAlign.CENTER,
                                                            weight=FontWeight.BOLD,
                                                            width=900,
                                                        ),
                                                    ],
                                                    vertical_alignment=CrossAxisAlignment.CENTER,
                                                ),
                                                width=1000,
                                                height=100,
                                                bgcolor=colors.BLUE_ACCENT_200,
                                                border_radius=5,
                                                alignment=alignment.center,
                                                padding=10,
                                            ),
                                            Icon(
                                                name=icons.GROUPS_2,
                                                color=colors.TEAL,
                                                size=50
                                            ),
                                            TextField(
                                                label="Nome",
                                                hint_text="Digite o nome do profissional",
                                                icon=icons.ABC_ROUNDED,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=50,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Profissão",
                                                hint_text="Digite a profissão",
                                                icon=icons.ABC_ROUNDED,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=50,
                                                border_radius=10,
                                            ),
                                            TextField(
                                                label="Especialidade",
                                                hint_text="Digite a especialidade do profissional",
                                                icon=icons.ABC_ROUNDED,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=50,
                                                border_radius=10,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value="CRM", label="CRM"),
                                                        Radio(value="CRO", label="CRO"),
                                                        Radio(value="CRF", label="CRF"),
                                                        Radio(value="CFM", label="CFM"),
                                                    ],
                                                    alignment=MainAxisAlignment.CENTER,
                                                )
                                            ),
                                            TextField(
                                                label="Conselho",
                                                hint_text="Digite o número de CRM ou CRO do profissional",
                                                icon=icons.ONETWOTHREE,
                                                bgcolor=colors.GREY_50,
                                                focused_bgcolor=colors.TEAL_50,
                                                border_color=colors.AMBER,
                                                focused_border_color=colors.TEAL,
                                                focused_color=colors.BLACK,
                                                capitalization=TextCapitalization.CHARACTERS,
                                                text_size=25,
                                                width=800,
                                                height=50,
                                                border_radius=10,
                                            ),
                                            ElevatedButton(
                                                text="Realizar Cadastro",
                                                icon=icons.CHECK_CIRCLE,
                                                bgcolor=colors.LIGHT_GREEN_ACCENT_100,
                                                color=colors.BLACK,
                                                width=300,
                                                height=60,
                                                on_click=cadastrarNovoProfissional
                                            )
                                        ],
                                        horizontal_alignment=CrossAxisAlignment.CENTER
                                    ),
                                ]
                            ),
                            width=1000,
                            height=600,
                            border_radius=10,
                            gradient=gradiente,
                            alignment=alignment.top_center,
                            padding=2
                        ),

                    ],
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    vertical_alignment=MainAxisAlignment.CENTER,
                    # scroll=ScrollMode.ALWAYS,
                ),
            )
        if page.route == "/listaPacientes":
            page.views.append(
                View(
                    "//listaPacientes",
                    [
                        Container(
                            content=Row(
                                controls=[
                                    IconButton(
                                        icon=icons.HOME,
                                        bgcolor=colors.BLUE_50,
                                        on_click=lambda _: page.go(ultima_rota[-1]),
                                    ),
                                    Text(
                                        value="Pacientes",
                                        color=colors.WHITE,
                                        size=40,
                                        font_family="Open Sans",
                                        text_align=TextAlign.CENTER,
                                        weight=FontWeight.BOLD,
                                        width=900,
                                    ),
                                ],
                                vertical_alignment=CrossAxisAlignment.CENTER,
                            ),
                            width=1000,
                            height=100,
                            bgcolor=colors.BLUE_ACCENT_200,
                            border_radius=5,
                            alignment=alignment.center,
                            padding=10,
                        ),
                        SearchBar(
                            bar_hint_text="Nome do paciente",
                            view_hint_text="Digite o nome de quem deseja pesquisar",
                            width=1000,
                            height=50,
                        ),
                        ResponsiveRow(
                            controls=[
                                GridView(
                                    controls=[
                                        DataTable(
                                            columns=[
                                                DataColumn(Text("CPF", size=20)),
                                                DataColumn(Text("Nome", size=20)),
                                                DataColumn(Text("Data de nascimento", size=20)),
                                                DataColumn(Text("Data de cadastro", size=20)),
                                            ],
                                            rows=[
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("123456789-10")),
                                                        DataCell(Text("Henrique Carvalho")),
                                                        DataCell(Text("22/04/1995")),
                                                        DataCell(Text("10/03/2024")),
                                                    ]
                                                ),
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("987654321-01")),
                                                        DataCell(Text("Pedro Gabriel Souza")),
                                                        DataCell(Text("10/05/2001")),
                                                        DataCell(Text("03/01/2024")),
                                                    ]
                                                ),
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("432198765-52")),
                                                        DataCell(Text("Antonio Pedro da Silva")),
                                                        DataCell(Text("22/04/1995")),
                                                        DataCell(Text("15/02/2024")),
                                                    ]
                                                ),

                                            ],
                                            border=border.all(1, "teal"),
                                            heading_row_color=colors.RED_100,
                                            border_radius=5,
                                        )
                                    ],
                                    expand=True,
                                ),
                            ],
                            width=1000,
                            height=400,
                        )
                        if str(ultima_rota[-1]) == "/telaInicialAtendente"
                        else
                        ResponsiveRow(
                            controls=[
                                GridView(
                                    controls=[
                                        DataTable(
                                            columns=[
                                                DataColumn(Text("CPF", size=20)),
                                                DataColumn(Text("Nome", size=20)),
                                                DataColumn(Text("Data de nascimento", size=20)),
                                                DataColumn(Text("Data de cadastro", size=20)),
                                                DataColumn(Text("Fotos Paciente", size=20)),
                                            ],
                                            rows=[
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("123456789-10")),
                                                        DataCell(Text("Henrique Carvalho")),
                                                        DataCell(Text("22/04/1995")),
                                                        DataCell(Text("10/03/2024")),
                                                        DataCell(
                                                            ElevatedButton(
                                                                text="Ver",
                                                                on_click=verFotoPaciente,
                                                                key="123456789-10",
                                                            )
                                                        ),
                                                    ]
                                                ),
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("987654321-01")),
                                                        DataCell(Text("Pedro Gabriel Souza")),
                                                        DataCell(Text("10/05/2001")),
                                                        DataCell(Text("03/01/2024")),
                                                        DataCell(
                                                            ElevatedButton(
                                                                text="Ver",
                                                                on_click=verFotoPaciente,
                                                                key="987654321-01",
                                                            )
                                                        ),
                                                    ]
                                                ),
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("432198765-52")),
                                                        DataCell(Text("Antonio Pedro da Silva")),
                                                        DataCell(Text("22/04/1995")),
                                                        DataCell(Text("15/02/2024")),
                                                        DataCell(
                                                            ElevatedButton(
                                                                text="Ver",
                                                                on_click=verFotoPaciente,
                                                                key="432198765-52",
                                                            )
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            border=border.all(1, "teal"),
                                            heading_row_color=colors.RED_100,
                                            border_radius=5,
                                        )
                                    ],
                                    expand=True,
                                ),
                            ],
                            width=1000,
                            height=400,
                        )

                    ],
                    vertical_alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
        if page.route == "/listaProfissionais":
            page.views.append(
                View(
                    "//listaProfissionais",
                    [
                        Container(
                            content=Row(
                                controls=[
                                    IconButton(
                                        icon=icons.HOME,
                                        bgcolor=colors.BLUE_50,
                                        on_click=lambda _: page.go(ultima_rota[-1]),
                                    ),
                                    Text(
                                        value="Profissionais",
                                        color=colors.WHITE,
                                        size=40,
                                        font_family="Open Sans",
                                        text_align=TextAlign.CENTER,
                                        weight=FontWeight.BOLD,
                                        width=900,
                                    ),
                                ],
                                vertical_alignment=CrossAxisAlignment.CENTER,
                            ),
                            width=1000,
                            height=100,
                            bgcolor=colors.BLUE_ACCENT_200,
                            border_radius=5,
                            alignment=alignment.center,
                            padding=10,
                        ),
                        SearchBar(
                            bar_hint_text="Conselho",
                            view_hint_text="Digite o nome do profissional que  deseja pesquisar",
                            width=1000,
                            height=50,
                        ),
                        ResponsiveRow(
                            controls=[
                                GridView(
                                    controls=[
                                        DataTable(
                                            columns=[
                                                DataColumn(Text("Nome", size=20)),
                                                DataColumn(Text("Especialidade", size=20)),
                                                DataColumn(Text("Conselho", size=20)),
                                                DataColumn(Text("Nº do conselho", size=20)),
                                            ],
                                            rows=[
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("Bernado Souza")),
                                                        DataCell(Text("Dentista")),
                                                        DataCell(Text("CRM")),
                                                        DataCell(Text("00000000-0")),
                                                    ]
                                                ),
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("Maria Leticia")),
                                                        DataCell(Text("Dermatologista")),
                                                        DataCell(Text("CRO")),
                                                        DataCell(Text("00000000-2233")),
                                                    ]
                                                ),
                                                DataRow(
                                                    cells=[
                                                        DataCell(Text("Mateus Rodrigues")),
                                                        DataCell(Text("Esteticista")),
                                                        DataCell(Text("CRF")),
                                                        DataCell(Text("00000000-3344")),
                                                    ]
                                                ),
                                            ],
                                            border=border.all(1, "teal"),
                                            heading_row_color=colors.RED_100,
                                            border_radius=5,
                                        )
                                    ],
                                    expand=True,
                                ),
                            ],
                            width=1000,
                            height=400,
                        )
                    ],
                    vertical_alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
        if page.route == "/fotosPaciente":
            page.views.append(
                View(
                    "/fotosPaciente",
                    [
                        Container(
                            content=Row(
                                controls=[
                                    IconButton(
                                        icon=icons.HOME,
                                        bgcolor=colors.BLUE_50,
                                        on_click=lambda _: page.go(ultima_rota[-1]),
                                    ),
                                    Text(
                                        value="Selecione a pasta de um dos pacientes",
                                        color=colors.WHITE,
                                        size=40,
                                        font_family="Open Sans",
                                        text_align=TextAlign.CENTER,
                                        weight=FontWeight.BOLD,
                                        width=900,
                                    ),
                                ],
                                vertical_alignment=CrossAxisAlignment.CENTER,
                            ),
                            width=1000,
                            height=100,
                            bgcolor=colors.BLUE_ACCENT_200,
                            border_radius=5,
                            alignment=alignment.center,
                            padding=10,
                        ),
                        pasta_paciente
                    ],
                    vertical_alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
        if page.route == "/cadastrarAnamnese":
            page.views.append(
                View(
                    "/cadastrarAnamnese",
                    [
                        Container(
                            content=Row(
                                controls=[
                                    IconButton(
                                        icon=icons.HOME,
                                        bgcolor=colors.BLUE_50,
                                        on_click=lambda _: page.go(ultima_rota[-1]),
                                    ),
                                    Text(
                                        value="Dr. Leonardo Castellani",
                                        color=colors.WHITE,
                                        size=40,
                                        font_family="Open Sans",
                                        text_align=TextAlign.CENTER,
                                        weight=FontWeight.BOLD,
                                        width=900,
                                    ),
                                ],
                                vertical_alignment=CrossAxisAlignment.CENTER,
                            ),
                            width=1000,
                            height=100,
                            bgcolor=colors.BLUE_ACCENT_200,
                            border_radius=5,
                            alignment=alignment.center,
                            padding=10,
                        ),
                        Container(
                            content=Column(
                                controls=[
                                    Row(
                                        controls=[
                                            Text(
                                                value="FEZ ALGUMA CIRURGIA RECENTEMENTE?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="TOMA ALGUM REMÉDIO??",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="TOMA ANTICONCEPCIONAL?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="ALERGIA A MEDICAMENTO?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="PROBLEMA DE PRESSÃO?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="FAZ TRATAMENTO MÉDICO?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="GESTANTE?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="PROBLEMA DE FIGADO OU RIM?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="FUMANTE?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="JÁ TEVE HEPATITE?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="TEM DIABETES?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="PROBLEMA CARDIACO?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            Text(
                                                value="TEM PROBLEMA RENAL?",
                                                width=300,
                                                text_align=TextAlign.START,
                                                weight=FontWeight.BOLD,
                                            ),
                                            RadioGroup(
                                                content=Row(
                                                    controls=[
                                                        Radio(value='SIM', label="SIM", fill_color=colors.GREEN),
                                                        Radio(value='NÃO', label="NÃO", fill_color=colors.RED),
                                                    ],
                                                )
                                            ),
                                            TextField(
                                                label='SE SIM, QUAL?',
                                                text_align=TextAlign.CENTER,
                                                width=300,
                                                text_size=15,
                                            )
                                        ],
                                        height=30,
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            TextField(
                                                label='DESCREVA OUTROS PROBLEMAS QUE ACHA IMPORTANTE DESTACAR',
                                                text_align=TextAlign.CENTER,
                                                width=800,
                                                text_size=15,
                                                multiline=True,
                                            )
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                    Row(
                                        controls=[
                                            ElevatedButton(
                                                text="Realizar Cadastro da ficha",
                                                icon=icons.CHECK_CIRCLE,
                                                bgcolor=colors.LIGHT_GREEN_ACCENT_100,
                                                color=colors.BLACK,
                                                width=300,
                                                height=60,
                                                on_click=cadastrarFicha
                                            )
                                        ],
                                        alignment=MainAxisAlignment.CENTER,
                                        vertical_alignment=CrossAxisAlignment.CENTER,
                                    ),
                                ]
                            ),
                            expand=True,
                            bgcolor=gradiente,
                        ),
                    ],
                    scroll=ScrollMode.AUTO,
                    vertical_alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )
        if page.route == "/uploadFotosPacientes":
            page.views.append(
                View(
                    "/uploadFotosPacientes",
                    [
                        container_upload_fotos_paciente,
                    ],
                    scroll=ScrollMode.AUTO,
                    vertical_alignment=MainAxisAlignment.START,
                    horizontal_alignment=CrossAxisAlignment.CENTER
                )
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


app(target=main)
