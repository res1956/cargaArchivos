use seguros
go

truncate table SG_FASECOLDA
--------------------------------------------
declare @h_registro varchar(max)
declare @h_col01 varchar(100)
declare @h_col02 varchar(100)
declare @h_pos integer
declare @h_texto01 varchar(500)
declare @h_texto02 varchar(500)
declare @h_textoFINAL varchar(max)

declare c1 cursor for 
select annio.column_name , b.column_name, annio.pos
from(
select a.column_name, rank() over (order by a.column_name desc) pos
from (
select top 32 column_name
from information_schema.columns 
where table_name='EAC_FASECOLDA_WK'
and column_name like '[1-9]%'
order by 1 desc )a )annio
inner join (
select column_name , rank () over (order by ordinal_position)pos 
from information_schema.columns 
where table_schema='dbo' and table_name='SG_FASECOLDA'
and column_name like 'Valor%') b on annio.pos=b.pos ;

open c1

fetch next from c1 into @h_col01, @h_col02, @h_pos

WHILE @@FETCH_STATUS=0
BEGIN
  if @h_pos=1 
      BEGIN
          set @h_texto01 = '[' + @h_col01 + ']'
		  set @h_texto02 = @h_col02
	  END 
  else
      BEGIN 
          set @h_texto01 = @h_texto01 + ','  + '[' + @h_col01 + ']'
		  set @h_texto02 = @h_texto02 + ','  + @h_col02
      END
fetch next from c1 into @h_col01, @h_col02, @h_pos
END


close c1
deallocate c1


set @h_texto02 =  ' insert into sg_fasecolda ( ' +  @h_texto02 + ', FechaInsert,  EstadoProceso , DescVehiculo ,  DesVehiculoTipo , DesVehiculoMarca, CodVehiculoExterno , CodHomologado, DesGrupoModelo) '
---------------------------------------------------------------

exec  ( @h_texto02 +  ' select ' + @h_texto01 + '
      , convert(varchar,getdate(),120)
	  , ''N''
	  , replace(Referencia2,'''''''','''''''''''') + '''' + replace(Referencia3,'''''''','''''''''''')
	  , clase , Marca , codigo , Homologocodigo, replace(Referencia1,'''''''','''''''''''')
	   from eac_fasecolda_wk ')

----------------------------------------------------------------

