# callback.py

from dash import Output, Input, State, PreventUpdate, callback

def create_callback(app, df_remessa, df_retorno, df_remessa_novo_nome, df_retorno_novo_nome):
    @app.callback(
        [Output('data-table-remessa', 'data'),
         Output('data-table-retorno', 'data')],
        [Input('pesquisar-doc-button', 'n_clicks')],
        [State('numero-boleto-input', 'value')],
        allow_duplicate=True
    )
    def update_table(n_clicks_doc, numero_boleto):
        ctx = dash.callback_context
        if not numero_boleto or n_clicks_doc == 0:
            return df_remessa.to_dict('records'), df_retorno.to_dict('records')

        if ctx.triggered_id == 'pesquisar-doc-button':
            resultado_pesquisa_remessa = df_remessa[df_remessa['CODIGO DO DOC'].astype(str) == numero_boleto]
            resultado_pesquisa_retorno = df_retorno[df_retorno['CODIGO DO DOC'].astype(str) == numero_boleto]
            return resultado_pesquisa_remessa.to_dict('records'), resultado_pesquisa_retorno.to_dict('records')
        else:
            raise PreventUpdate
