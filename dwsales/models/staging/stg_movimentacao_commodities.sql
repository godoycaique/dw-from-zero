with source as (
    select 
        date,
        symbol,
        action,
        quantity
    from
        {{ source('dbsales_wvdl', 'movimentacao_commodities') }}
),

renamed as (
    select
        cast(date as date) as data,
        symbol as simbolo,
        action as acao,
        quantity as quantidade
    from source
)

select * from renamed