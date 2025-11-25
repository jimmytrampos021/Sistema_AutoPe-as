/**
 * Script JavaScript para o Admin de Produtos
 * Melhora a UX com cálculos automáticos e validações
 */

(function($) {
    $(document).ready(function() {
        
        // ==========================================
        // CÁLCULO AUTOMÁTICO DE PREÇOS
        // ==========================================
        
        /**
         * Calcula preço com taxa
         */
        function calcularPrecoComTaxa(precoBase, taxaPercentual) {
            if (!precoBase || precoBase <= 0) return 0;
            const taxa = taxaPercentual / 100;
            return precoBase * (1 + taxa);
        }
        
        /**
         * Tabela de taxas (mesma do banco de dados)
         */
        const TAXAS = {
            'DEBITO': 1.09,
            'CREDITO': {
                1: 3.45,
                2: 5.18,
                3: 6.37,
                4: 7.56,
                5: 8.75,
                6: 9.94,
                7: 11.13,
                8: 12.32,
                9: 13.51,
                10: 14.70,
                11: 15.89,
                12: 17.08
            }
        };
        
        /**
         * Atualiza sugestões de preços automaticamente
         */
        function atualizarSugestoesPrecos() {
            const precoVista = parseFloat($('#id_preco_venda_dinheiro').val()) || 0;
            
            if (precoVista <= 0) return;
            
            // Calcula débito
            const precoDebito = calcularPrecoComTaxa(precoVista, TAXAS.DEBITO);
            
            // Calcula crédito à vista
            const precoCredito1x = calcularPrecoComTaxa(precoVista, TAXAS.CREDITO[1]);
            
            // Mostra sugestões próximas aos campos
            mostrarSugestao('id_preco_venda_debito', precoDebito);
            mostrarSugestao('id_preco_venda_credito', precoCredito1x);
            
            // Se "Preços Customizados" estiver desmarcado, calcula todas as parcelas
            const usaCustomizado = $('#id_preco_customizado_cartao').is(':checked');
            
            if (!usaCustomizado) {
                for (let parcela = 2; parcela <= 12; parcela++) {
                    const precoParcelado = calcularPrecoComTaxa(precoVista, TAXAS.CREDITO[parcela]);
                    mostrarSugestao(`id_preco_credito_${parcela}x`, precoParcelado);
                }
            }
        }
        
        /**
         * Mostra sugestão de preço ao lado do campo
         */
        function mostrarSugestao(fieldId, valor) {
            const $field = $(`#${fieldId}`);
            if ($field.length === 0) return;
            
            // Remove sugestão antiga
            $field.next('.sugestao-preco').remove();
            
            // Só mostra se o campo estiver vazio
            const valorAtual = parseFloat($field.val()) || 0;
            
            if (valorAtual === 0 && valor > 0) {
                const $sugestao = $('<span class="sugestao-preco"></span>');
                $sugestao.html(`
                    <span style="color: #28a745; font-size: 0.9rem; margin-left: 10px;">
                        💡 Sugestão: R$ ${valor.toFixed(2)}
                        <a href="#" class="aplicar-sugestao" data-field="${fieldId}" data-valor="${valor.toFixed(2)}" 
                           style="color: #0d6efd; text-decoration: underline; margin-left: 5px;">Aplicar</a>
                    </span>
                `);
                $field.after($sugestao);
            }
        }
        
        /**
         * Aplica sugestão ao clicar
         */
        $(document).on('click', '.aplicar-sugestao', function(e) {
            e.preventDefault();
            const fieldId = $(this).data('field');
            const valor = $(this).data('valor');
            
            $(`#${fieldId}`).val(valor).trigger('change');
            $(this).closest('.sugestao-preco').fadeOut(300, function() {
                $(this).remove();
            });
        });
        
        /**
         * Monitora mudanças no preço à vista
         */
        $('#id_preco_venda_dinheiro').on('change keyup', function() {
            setTimeout(atualizarSugestoesPrecos, 300);
        });
        
        /**
         * Monitora mudanças no checkbox de preços customizados
         */
        $('#id_preco_customizado_cartao').on('change', function() {
            const usaCustomizado = $(this).is(':checked');
            const $fieldset = $('.field-preco_credito_2x').closest('fieldset');
            
            if (usaCustomizado) {
                $fieldset.removeClass('collapsed');
                $fieldset.find('h2').css('background-color', '#fff3cd');
            } else {
                $fieldset.find('h2').css('background-color', '');
            }
            
            atualizarSugestoesPrecos();
        });
        
        // Executa na inicialização
        setTimeout(atualizarSugestoesPrecos, 500);
        
        
        // ==========================================
        // VALIDAÇÕES E AVISOS
        // ==========================================
        
        /**
         * Valida se preço de custo < preço de venda
         */
        function validarMargem() {
            const precoCusto = parseFloat($('#id_preco_custo').val()) || 0;
            const precoVenda = parseFloat($('#id_preco_venda_dinheiro').val()) || 0;
            
            if (precoCusto > 0 && precoVenda > 0 && precoCusto >= precoVenda) {
                mostrarAviso('id_preco_venda_dinheiro', 
                    '⚠️ ATENÇÃO: Preço de venda está menor ou igual ao custo! Você terá prejuízo.', 
                    'warning');
            } else {
                removerAviso('id_preco_venda_dinheiro');
                
                // Mostra margem de lucro
                if (precoCusto > 0 && precoVenda > 0) {
                    const margem = ((precoVenda - precoCusto) / precoCusto) * 100;
                    mostrarAviso('id_preco_venda_dinheiro', 
                        `✅ Margem de lucro: ${margem.toFixed(2)}%`, 
                        'success');
                }
            }
        }
        
        /**
         * Mostra aviso colorido
         */
        function mostrarAviso(fieldId, mensagem, tipo) {
            const $field = $(`#${fieldId}`);
            if ($field.length === 0) return;
            
            removerAviso(fieldId);
            
            const cores = {
                'success': '#d4edda',
                'warning': '#fff3cd',
                'danger': '#f8d7da'
            };
            
            const $aviso = $('<div class="aviso-campo"></div>');
            $aviso.html(`
                <div style="background: ${cores[tipo]}; padding: 8px 12px; border-radius: 4px; margin-top: 5px; font-size: 0.9rem;">
                    ${mensagem}
                </div>
            `);
            
            $field.closest('.field-preco_venda_dinheiro, .field-preco_custo').append($aviso);
        }
        
        /**
         * Remove aviso
         */
        function removerAviso(fieldId) {
            $(`#${fieldId}`).closest('.field-preco_venda_dinheiro, .field-preco_custo').find('.aviso-campo').remove();
        }
        
        // Monitora mudanças para validação
        $('#id_preco_custo, #id_preco_venda_dinheiro').on('change keyup', function() {
            setTimeout(validarMargem, 300);
        });
        
        
        // ==========================================
        // BOTÃO DE AÇÃO RÁPIDA
        // ==========================================
        
        /**
         * Adiciona botão para calcular todos os preços automaticamente
         */
        function adicionarBotaoCalcularTodos() {
            const $precoVista = $('#id_preco_venda_dinheiro').closest('.form-row');
            
            if ($precoVista.length && !$('#btn-calcular-todos').length) {
                const $botao = $(`
                    <div style="margin-top: 10px;">
                        <button type="button" id="btn-calcular-todos" class="button" style="background: #28a745; color: white;">
                            ⚡ Calcular todos os preços automaticamente
                        </button>
                        <p style="font-size: 0.85rem; color: #6c757d; margin-top: 5px;">
                            Preenche automaticamente débito, crédito e todos os parcelamentos com base no preço à vista
                        </p>
                    </div>
                `);
                
                $precoVista.after($botao);
            }
        }
        
        /**
         * Executa cálculo de todos os preços
         */
        $(document).on('click', '#btn-calcular-todos', function(e) {
            e.preventDefault();
            
            const precoVista = parseFloat($('#id_preco_venda_dinheiro').val()) || 0;
            
            if (precoVista <= 0) {
                alert('⚠️ Por favor, defina o preço à vista primeiro!');
                $('#id_preco_venda_dinheiro').focus();
                return;
            }
            
            // Calcula e preenche débito
            const precoDebito = calcularPrecoComTaxa(precoVista, TAXAS.DEBITO);
            $('#id_preco_venda_debito').val(precoDebito.toFixed(2));
            
            // Calcula e preenche crédito à vista
            const precoCredito1x = calcularPrecoComTaxa(precoVista, TAXAS.CREDITO[1]);
            $('#id_preco_venda_credito').val(precoCredito1x.toFixed(2));
            
            // Calcula parcelamentos se "Preços Customizados" estiver marcado
            if ($('#id_preco_customizado_cartao').is(':checked')) {
                for (let parcela = 2; parcela <= 12; parcela++) {
                    const precoParcelado = calcularPrecoComTaxa(precoVista, TAXAS.CREDITO[parcela]);
                    $(`#id_preco_credito_${parcela}x`).val(precoParcelado.toFixed(2));
                }
            }
            
            // Mostra mensagem de sucesso
            const $mensagem = $(`
                <div style="background: #d4edda; color: #155724; padding: 12px; border-radius: 4px; margin-top: 10px; animation: fadeIn 0.3s;">
                    ✅ Preços calculados com sucesso!
                </div>
            `);
            
            $(this).after($mensagem);
            setTimeout(function() {
                $mensagem.fadeOut(300, function() { $(this).remove(); });
            }, 3000);
        });
        
        // Adiciona botão na inicialização
        setTimeout(adicionarBotaoCalcularTodos, 500);
        
        
        // ==========================================
        // DESTAQUE VISUAL PARA IMPOSTO 4%
        // ==========================================
        
        /**
         * Destaca fieldset quando imposto 4% está ativo
         */
        function destacarImposto4() {
            const imposto4Ativo = $('#id_aplicar_imposto_4').is(':checked');
            const $fieldset = $('.field-aplicar_imposto_4').closest('fieldset');
            
            if (imposto4Ativo) {
                $fieldset.css({
                    'border': '2px solid #dc3545',
                    'background': '#fff5f5'
                });
                
                // Adiciona aviso visual
                if (!$('#aviso-imposto-4').length) {
                    $fieldset.prepend(`
                        <div id="aviso-imposto-4" style="background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; margin-bottom: 10px;">
                            <strong>⚠️ IMPOSTO DE 4% ATIVO</strong><br>
                            Todos os preços de venda terão 4% adicional calculado automaticamente.
                        </div>
                    `);
                }
            } else {
                $fieldset.css({
                    'border': '',
                    'background': ''
                });
                $('#aviso-imposto-4').remove();
            }
        }
        
        $('#id_aplicar_imposto_4').on('change', destacarImposto4);
        setTimeout(destacarImposto4, 500);
        
    });
})(django.jQuery);
