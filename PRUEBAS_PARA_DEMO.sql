select [2025],[2024],[2023],[2022],[2021],[2020],[2019],[2018],[2017],[2016],[2015],[2014],[2013],[2012],[2011],[2010],[2009],[2008],[2007],[2006],[2005],[2004],[2003],[2002],[2001],[2000],[1999],[1998],[1997],[1996],[1995],[1994]
      , convert(varchar,getdate(),120)
	  , 'N'
	  , replace(Referencia2,'''','''''')
	   from eac_fasecolda_wk 

where referencia2 like '%'' EAGLE%'

truncate table sg_fasecolda
 insert into sg_fasecolda ( Valor_0Km,Valor_0,Valor_1,Valor_2,Valor_3,Valor_4,Valor_5,Valor_6,Valor_7,Valor_8,Valor_9,Valor_10,Valor_11,Valor_12,Valor_13,Valor_14,Valor_15,Valor_16,Valor_17,Valor_18,Valor_19,Valor_20,Valor_21,Valor_22,Valor_23,Valor_24,Valor_25,Valor_26,Valor_27,Valor_28,Valor_29,Valor_30, FechaInsert,  EstadoProceso , DescVehiculo ,  DesVehiculoTipo , DesVehiculoMarca, CodVehiculoExterno , CodHomologado, DesGrupoModelo)   
 select [2025],[2024],[2023],[2022],[2021],[2020],[2019],[2018],[2017],[2016],[2015],[2014],[2013],[2012],[2011],[2010],[2009],[2008],[2007],[2006],[2005],[2004],[2003],[2002],[2001],[2000],[1999],[1998],[1997],[1996],[1995],[1994]
      , convert(varchar,getdate(),120)
	  , 'N'
	  , replace(Referencia2,'''','''''') + '' + replace(Referencia3,'''','''''')
	  , clase , Marca , codigo , Homologocodigo, replace(Referencia1,'''','''''')
	   from eac_fasecolda_wk 


