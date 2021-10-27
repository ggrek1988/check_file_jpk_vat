<?xml version="1.0" encoding="utf-8"?>
<!-- $Id: faktura_sprzedazowa_pdf.xsl,v 1.1.2.8 2011/03/07 16:43:11 mariusz Exp $ -->
<xsl:stylesheet version="1.1" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:fo="http://www.w3.org/1999/XSL/Format" exclude-result-prefixes="fo">
	<xsl:output method="xml" version="1.0" omit-xml-declaration="no" indent="yes" encoding="UTF-8"/>
	<xsl:param name="versionParam" select="'1.0'"/> 
	<!-- ========================= -->
	<!-- root element: Invoice -->
	<!-- ========================= -->
	<xsl:template match="invoice">
		<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format" font-family="Times" font-weight="bold" >
			<fo:layout-master-set>
				<fo:simple-page-master master-name="simpleA4" page-height="29.7cm" page-width="21cm" margin-top="1cm" margin-bottom="0.8cm" margin-left="1cm" margin-right="1cm">
					<fo:region-body/>
						<fo:region-after extent="0.1cm"/>
				</fo:simple-page-master>
				</fo:layout-master-set>
			<fo:page-sequence master-reference="simpleA4">
				
					<fo:static-content flow-name="xsl-region-after">
			      <fo:block line-height="5pt" font-size="5pt" text-align="end" space-before="2mm">
			      		<fo:block line-height="5pt" font-size="5pt" text-align="left" space-before="2mm">
									LeftHand-System (http://www.lefthand.com.pl)
									
					</fo:block>
			      </fo:block>
			    </fo:static-content>
			    
				<fo:flow flow-name="xsl-region-body">
					
					<fo:block font-weight="bold" text-align="left" vertical-align="middle">
											 
										<fo:external-graphic src="logo.gif" content-height="scale-to-fit" height="0.50in"  content-width="1.80in" scaling="non-uniform"/>
    					    
										</fo:block>
				
					<!-- begin FLOW	-->
					<fo:block font-family="Times" space-after="0mm" text-align="center">
					
						<fo:table table-layout="fixed" font-size="6pt">
							<fo:table-column column-width="20%"/>
							<fo:table-column column-width="65%"/>
							<fo:table-column column-width="15%"/>

							
							<fo:table-body>
								<fo:table-row>
									<fo:table-cell border-width="0pt" 	border-style="solid" border-color="black" padding="0 pt">
										<fo:block font-weight="bold" text-align="center" vertical-align="middle">
											 
										&#160;
    					    
										</fo:block>
									</fo:table-cell>
									<fo:table-cell border-width="0pt" 	border-style="solid" border-color="black" padding="0pt">
										<fo:block font-weight="bold" font-size="13pt" text-align="center" vertical-align="middle">
											Raport podsumowujacy sprawdzenie kontrahentow z dnia: 
										</fo:block>
									</fo:table-cell>
									<fo:table-cell border-width="0pt" 	border-style="solid" border-color="black" padding="0pt">
										<fo:block font-weight="bold" font-size="13pt" text-align="center" vertical-align="middle">
											<xsl:value-of select="data"/>
										</fo:block>
									</fo:table-cell>
								
									
								</fo:table-row>
							</fo:table-body>
							
					
							
						</fo:table>
					<fo:inline font-family="Times" font-size="13pt" text-align="center" ></fo:inline>
					</fo:block>
					<fo:block font-family="Times" space-after="1mm" text-align="center">
					
					&#160;
					</fo:block>
					<fo:block font-family="Times" space-after="1mm" text-align="center">
					
					&#160;
					</fo:block>
					
					
					
					<fo:block font-family="Times" space-after="1mm" text-align="center">
					<xsl:if test="validation = '0'">
					<fo:inline font-family="Times" background-color="#03fc18" font-size="13pt" text-align="center" >Numery NIP zweryfikowane pozytywnie</fo:inline>
					</xsl:if>
					<xsl:if test="validation = '1'">
					<fo:inline font-family="Times" background-color="#fc0303" font-size="13pt" text-align="center" >Numery NIP zweryfikowane negatywnie</fo:inline>
					</xsl:if>
					</fo:block>
					
					<fo:block font-family="Times" space-after="1mm" text-align="center">
					&#160;
					</fo:block>
					<fo:block font-family="Times" space-after="1mm" text-align="center">
					
					&#160;
					</fo:block>
					

				
					
					
					<!--          tu koniec         -->
					
					<!--  Tabela z pozycjami faktury  -->
						<fo:table table-layout="fixed" font-size="8pt">
							<fo:table-column column-width="5%"/>
							<fo:table-column column-width="20%"/>
							<fo:table-column column-width="40%"/>
							<fo:table-column column-width="10%"/>
							<fo:table-column column-width="20%"/>
							<fo:table-column column-width="5%"/>
							<fo:table-header>
								<fo:table-row>
									<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
										<fo:block font-weight="bold" text-align="center" vertical-align="middle">
											Lp.
										</fo:block>
									</fo:table-cell>
									<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
										<fo:block font-weight="bold" text-align="center" vertical-align="middle">
											NIP kontrahenta
										</fo:block>
									</fo:table-cell>
									<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
										<fo:block font-weight="bold" text-align="center" vertical-align="middle">
											Status
										</fo:block>
									</fo:table-cell>
									<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
										<fo:block font-weight="bold" text-align="center" vertical-align="middle">
											Werfikacja
										</fo:block>
									</fo:table-cell>
									<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
										<fo:block font-weight="bold" text-align="center" vertical-align="middle">
											Data weryfikacji
										</fo:block>
									</fo:table-cell>
									<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
										<fo:block font-weight="bold" text-align="center" vertical-align="middle">
											Zrodlo
										</fo:block>
									</fo:table-cell>
									
								</fo:table-row>
							</fo:table-header>
					
							<fo:table-body>
								<xsl:apply-templates select="positions/position"/>
							</fo:table-body>
					
							
						</fo:table>
					
				

					
					

				</fo:flow>
			</fo:page-sequence>
		</fo:root>
	</xsl:template>

	<!-- ========================= -->
	<!-- loop: positions/position  -->
	<!-- ========================= -->
	<xsl:template match="positions/position">
		<fo:table-row>
			<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
				<fo:block text-align="center" vertical-align="middle" font-weight="normal">
					<xsl:value-of select="id"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
				<fo:block text-align="left" vertical-align="middle" font-weight="normal">
					<xsl:value-of select="name"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
				<fo:block text-align="left" vertical-align="middle" font-weight="normal">
					<xsl:value-of select="status"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">

				
				<xsl:if test="code = 'Z'">
						<fo:block  text-align="right" background-color="#03fc18" vertical-align="middle" wrap-option="wrap">
							&#160;
						</fo:block>
					</xsl:if>
				<xsl:if test="code = 'C'">
						<fo:block  text-align="right" background-color="#fc0303" vertical-align="middle" wrap-option="wrap">
							&#160;
						</fo:block>
					</xsl:if>
				<xsl:if test="code = 'S'">
						<fo:block  text-align="right" background-color="##b3b1b1" vertical-align="middle" wrap-option="wrap">
							&#160;
						</fo:block>
					</xsl:if>
				<xsl:if test="code = ''">
					<fo:block  text-align="right" background-color="##b3b1b1" vertical-align="middle" wrap-option="wrap">
						&#160;
					</fo:block>
				</xsl:if>
			</fo:table-cell>
			<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
				<fo:block text-align="center" vertical-align="middle" font-weight="normal">
					<xsl:value-of select="date_w"/>
				</fo:block>
			</fo:table-cell>
			<fo:table-cell border-width="0.25pt" 	border-style="solid" border-color="black" padding="2pt">
				<fo:block text-align="center" vertical-align="middle" font-weight="normal">
					<xsl:value-of select="source"/>
				</fo:block>
			</fo:table-cell>
			
					
		</fo:table-row>
	</xsl:template>


	
</xsl:stylesheet>
