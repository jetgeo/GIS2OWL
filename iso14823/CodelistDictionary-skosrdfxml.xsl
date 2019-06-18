<?xml version="1.0" encoding="utf-8"?>
<!-- (c) 2009 interactive instruments GmbH - - Kent2017 -->
<xsl:stylesheet version="1.0" 
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
xmlns:gml="http://www.opengis.net/gml/3.2" 
xmlns:xlink="http://www.w3.org/1999/xlink" 
xmlns:skos="http://www.w3.org/2004/02/skos/core#"
xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
xmlns:xml="http://www.w3.org/XML/1998/namespace">
	<xsl:output method="html"/>
	<xsl:template match="/">
		<html>
			<head>
				<title>SKOS from «CodeList» <xsl:value-of select="/rdf:RDF/skos:ConceptScheme/skos:prefLabel"/></title>
			</head>
			<body>
				<h3>SKOS from «CodeList» <xsl:value-of select="/rdf:RDF/skos:ConceptScheme/skos:prefLabel"/></h3>
				<h3>Codelist namespace '<xsl:value-of select="/rdf:RDF/@xml:base"/>'</h3>
				<xsl:if test="/rdf:RDF/skos:ConceptScheme/skos:definition">
					<p><xsl:value-of select="/rdf:RDF/skos:ConceptScheme/skos:definition"/></p>
				</xsl:if>
				<table>
					<tr>
						<td  width="300">
							<u>Code Name</u>
						</td>
						<td width="10">
							<br/>
						</td>
						<td  width="300">
							<u>Presenation Name</u>
						</td>
						<td width="10">
							<br/>
						</td>
						<td  width="300">
							<u>Definition</u>
						</td>
					</tr>
					<xsl:for-each select="/rdf:RDF/skos:Concept">
						<xsl:sort select="rdf:about[count(@codeSpace)=1]" data-type="number"/>
						<tr>
							<td valign="top">
								<xsl:choose>
								<!--xsl:when test="substring-before(skos:definition,'[DESC]')">
									<xsl:value-of select="substring-before(skos:definition,'[DESC]')"/>
									<br/>NOTE: <xsl:value-of select="substring-after(skos:definition,'[DESC]')"/>
								</xsl:when-->
								<xsl:when test="@rdf:about">
									<xsl:value-of select="@rdf:about"/>
								</xsl:when>
								<!--xsl:when test="skos:definition">
									<xsl:value-of select="skos:definition"/>
								</xsl:when-->
								</xsl:choose>
							</td>
							<td width="100">
								<br/>
							</td>
							<td valign="top">
								<xsl:value-of select="skos:prefLabel"/>
							</td>
							<td width="100">
								<br/>
							</td>
							<td valign="top">
								<xsl:choose>
								<xsl:when test="substring-before(/rdf:RDF/skos:Concept/@rdf:about,/rdf:RDF/skos:ConceptScheme/@rdf:about+'/')">
									<xsl:value-of select="substring-before(/rdf:RDF/skos:Concept/@rdf:about,'/')"/>
									<br/>NOTE: <xsl:value-of select="substring-after(/rdf:RDF/skos:Concept/@rdf:about,/rdf:RDF/skos:ConceptScheme/@rdf:about+'/')"/>
								</xsl:when>
								<xsl:when test="/skos:Concept/@rdf:about">
									<xsl:value-of select="/skos:Concept/@rdf:about"/>
								</xsl:when>
								<xsl:when test="skos:definition">
									<xsl:value-of select="skos:definition"/>
								</xsl:when>
								</xsl:choose>
							</td>
						</tr>
					</xsl:for-each>
				</table>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>
